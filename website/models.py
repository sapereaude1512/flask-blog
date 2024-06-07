from . import db # dot (.) stands for the current package (in this case - website)
from flask_login import UserMixin # easily login and logout users
from sqlalchemy.sql import func

class User(db.Model, UserMixin): # model of the table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True) # maximum lenght is 50 characters
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # func.now gives the current time
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # if you do not put foreign key you could have posts from user that is deleted
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False) # lenght of the comment is restricted to 200 characters, so there'll be no extra long comments
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)