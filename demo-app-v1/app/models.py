from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(10))
    picture = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy="dynamic")
    def __init__(self,email,password):
        self.email = email
        self.password = password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40), unique=True)
    title = db.Column(db.String(255), unique=True)
    content = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Defining one to many relationship
    comments = db.relationship('Comment', backref="post", lazy="dynamic")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

