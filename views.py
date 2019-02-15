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
    return render_template('library.html', user=current_user)

@app.route('/store')
def store():
    games = Game.select().order_by(Game.title)
    return render_template('store.html', user=current_user, games=games)

@app.route('/game/<int:id>')
def game(id):
    return render_template('game.html', user=current_user)

@app.route('/purchase/<int:id>')
@login_required
def purchase(id):
    return render_template('purchase.html', user=current_user)

@app.route('/transaction') # random hash?
@login_required
def transaction():
    return render_template('transaction.html', user=current_user)

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
        Game(title=title, description=desc, genres=genres, price=price, developer=current_user)
        return redirect(url_for('created'))
    return render_template('dev_game_new.html', user=current_user, form=form)

@app.route('/dev/game/<int:id>')
@login_required
def dev_game(id):
    if not current_user.is_developer:
        return redirect('index')
    return render_template('dev_game.html', user=current_user)

