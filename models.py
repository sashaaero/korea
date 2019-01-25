from pony.orm import *
from flask_login import UserMixin

db = Database()


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    login = Required(str)
    email = Required(str)
    pwd = Required(str)
    scores = Set('Score')
    games = Set('Game')
    transactions = Set('Transaction')


class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    description = Required(str)
    genres = Required(str)
    scores = Set('Score')
    users = Set(User)
    price = Optional(int)
    developer = Required('Developer')


class Score(db.Entity):
    id = PrimaryKey(int, auto=True)
    game = Required(Game)
    user = Required(User)
    value = Optional(int)
    text = Optional(str)


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    type = Required(str)
    value = Required(int)
    user = Required(User)
    description = Optional(str)


class Developer(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    games = Set(Game)
    description = Optional(str)
