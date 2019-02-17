from flask import Flask, render_template, request, url_for, redirect
from pony.flask import Pony
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from models import *
from forms import *

app = Flask(__name__)
app.secret_key = 'asd&*$VNkhvrhk*V#__w3vqlbq;1'
pony = Pony(app)
manager = LoginManager(app)

@manager.user_loader
def load_user(user_id):
    return User.get(id=user_id)


@app.route('/')
def index():
    return redirect(url_for('store'))


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate():
        User(login=form.data['login'], email=form.data['email'], pwd=form.data['pwd1'], is_developer=False)
        return redirect(url_for('login'))
    return render_template('reg.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(login=form.data['login'])
        pwd = form.data['pwd']
        if user.pwd != pwd:
            return 'Incorrect password'
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@app.route('/dev/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/library')
@login_required
def library():
    games = select(g for g in Game if g in current_user.games_owned).order_by(Game.title)
    # games = current_user.games_owned
    return render_template('library.html', user=current_user, games=games)

@app.route('/store')
def store():
    games = Game.select().order_by(Game.title)
    return render_template('store.html', user=current_user, games=games)

@app.route('/game/<int:id>')
def game(id):
    game = Game.get(id=id)
    scores = select(s for s in Score if s.game == game).order_by(Score.dt)
    if game is None:
        return redirect(page_not_found)
    return render_template('game.html', user=current_user, game=game, scores=scores)

@app.route('/post_score', methods=['POST'])
def post_score():
    game_id = request.form['id']
    score = request.form['score']
    text = request.form['text']
    game = Game.get(id=game_id)
    print(game_id)
    if game is not None:
        Score(game=game, value=int(score), text=text, user=current_user, dt=datetime.now())
    return redirect(url_for('game', id=game_id))

@app.route('/purchase/<int:id>')
@login_required
def purchase(id):
    game = Game.get(id=id)
    user = current_user
    if game not in user.games_owned:
        if user.money >= game.price:
            Transaction(type='Buy', value=-game.price, user=user, description=game.title, dt=datetime.now())
            user.money -= game.price
            user.games_owned.add(game)
    return redirect(url_for('game', id=id))

@app.route('/add_funds', methods=['POST', 'GET'])
@login_required
def add_funds():
    if request.method == 'POST':
        money = request.form['funds']
        try:
            money = int(money)
        except:
            money = 0
        t = Transaction(type='Add', value=money, user=current_user, dt=datetime.now())
        current_user.money += money
        return redirect(url_for('index'))
    return render_template('add_funds.html', user=current_user)

@app.route('/transactions')
@login_required
def transactions():
    t = select(t for t in Transaction if t.user == current_user).order_by(Transaction.dt)[:]
    return render_template('transaction.html', user=current_user, transactions=t)

# @app.route('/transaction') # random hash?
# @login_required
# def transaction():
#     return render_template('transaction.html', user=current_user)

@app.route('/dev/reg', methods=['POST', 'GET'])
def dev_reg():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate():
        User(login=form.data['login'], email=form.data['email'], pwd=form.data['pwd1'], is_developer=True)
        return redirect(url_for('dev_login'))
    return render_template('dev_reg.html', form=form)

@app.route('/dev/login', methods=['POST', 'GET'])
def dev_login():
    form = DevLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(login=form.data['title'], pwd=form.data['pwd'])
        login_user(user)
        return redirect(url_for('index'))
    return render_template('dev_login.html', form=form)

@app.route('/dev/games_created')
@login_required
def created():
    if not current_user.is_developer:
        return redirect(url_for('index'))

    games = select(g for g in Game if g.developer == current_user).prefetch(Score)[:]
    return render_template('dev_created.html', user=current_user, games=games)

@app.route('/dev/game/new', methods=['POST', 'GET'])
@login_required
def dev_game_new():
    if not current_user.is_developer:
        return redirect('index')

    form = DevNewGameForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.data['title']
        desc = form.data['description']
        genres = form.data['genres']
        price = form.data['price']
        small = form.data['small'] or None
        cover = form.data['cover'] or None
        Game(title=title, description=desc, genres=genres, price=price, developer=current_user, small=small, cover=cover)
        return redirect(url_for('created'))
    return render_template('dev_game_new.html', user=current_user, form=form)

@app.route('/dev/game/<int:id>', methods=['POST', 'GET'])
@login_required
def dev_game(id):
    if not current_user.is_developer:
        return redirect('index')
    # game = Game.get(id=id)
    game = select(g for g in Game if g.id == id).prefetch(Score, Game.developer).first()
    if game is None:
        return redirect(page_not_found)
    if game.developer.id != current_user.id:
        return redirect(url_for('game', id=id))

    if request.method == 'POST':
        game.title = request.form['title']
        game.desc = request.form['description']
        game.genres = request.form['genres']
        game.price = request.form['price']
        game.small = request.form['small'] or None
        game.cover = request.form['cover'] or None
    return render_template('dev_game.html', user=current_user, game=game)

@app.route('/dev/delete_score/<int:game_id>/<int:score_id>')
@login_required
def dev_delete_score(game_id, score_id):
    game = Game.get(id=game_id)
    if game is None or game.developer.id != current_user.id:
        return redirect(url_for('game', id=game_id))
    delete(s for s in Score if s.id == score_id)
    return redirect(url_for('game', id=game_id))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

