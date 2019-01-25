from flask import Flask, render_template
from pony.flask import Pony
from models import *

app = Flask(__name__)
pony = Pony(app)


@app.route('/')
def index():
    user = "Лох"
    return render_template('index.html', user=user)
