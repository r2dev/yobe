from . import db, login_manager
from datetime import datetime
from flask.ext.login import AnonymousUserMixin, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class User(UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	followed = db.relationship('Follow',
		foreign_keys=[Follow.follower_id],
		backref=db.backref('follower', lazy='joined'),
		lazy='dynamic',
		cascade='all, delete-orphan')
	followers = db.relationship('Follow',
		foreign_keys=[Follow.followed_id],
		backref=db.backref('followed', lazy='joined'),
		lazy='dynamic',
		cascade='all, delete-orphan')
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username
	def __init__(self, email, username, password):
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.email = email
	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)
	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.id).first()
		if f:
			db.session.delete(f)
	def is_following(self, user):
		return self.followed.filter_by(
			followed_id=user.id).first() is not None
	def is_followed_by(self, user):
		return self.followers.filter_by(
			follower_id=user.id).first() is not None
	

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

login_manager.anonymous_user = AnonymousUserMixin


