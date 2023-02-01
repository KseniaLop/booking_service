from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    data = db.Column(db.String(1024))
    free_sits_count = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Film {}>'.format(self.name)
