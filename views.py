from flask import Flask, render_template, request, url_for, redirect
from pony.flask import Pony
from models import *
from forms import *

app = Flask(__name__)
pony = Pony(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form)
        return redirect(url_for('index'))
    return render_template('reg.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/game/<int:id>')
def game(id):
    return render_template('game.html')

@app.route('/purchase/<int:id>')
def purchase(id):
    return render_template('purchase.html')

@app.route('/transaction') # random hash?
def transaction():
    return render_template('transaction.html')

@app.route('/dev/reg')
def dev_reg():
    return render_template('dev_reg.html')

@app.route('/dev/login')
def dev_login():
    return render_template('dev_login.html')

@app.route('/dev/game/new')
def dev_game_new():
    return render_template('dev_game_new.html')

@app.route('/dev/game/<int:id>')
def dev_game(id):
    return render_template('dev_game.html')

