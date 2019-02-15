from pony.orm import *
from flask_login import UserMixin

db = Database()


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    login = Required(str)
    email = Required(str)
    pwd = Required(str)
    is_developer = Required(bool, default=False)
    description = Optional(str)  # dev desc
    scores = Set('Score')
    games_owned = Set('Game', reverse='users')
    games_created = Set('Game', reverse='developer')
    transactions = Set('Transaction')


class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    description = Required(str)
    genres = Required(str)
    scores = Set('Score')
    users = Set(User)
    price = Optional(int)
    small = Optional(str)
    cover = Optional(str)
    developer = Required(User)


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
