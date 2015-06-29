
from flask import render_template, url_for, redirect
from flask.ext.login import current_user
from ..models import Post, User
from .. import db
from .forms import PostForm
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data, 
			author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	posts = Post.query.filter_by(author_id=current_user.get_id()).order_by(
		Post.timestamp.desc())
	return render_template('index.html', form=form, posts=posts)
@main.route('/following')
def following():
	pass
@main.route('/user/<int:user_id>')
def user(user_id):
	posts = Post.query.filter_by(author_id=user_id).order_by(
		Post.timestamp.desc())
	return render_template('user.html', posts=posts, user_id=user_id)

@main.route('/user/<int:user_id>/follow')
def follow(user_id):
	user = User.query.filter_by(id=user_id).first()
	current_user.follow(user)
	return redirect(url_for('user.observe', user_id=user_id))

@main.route('/user/<int:user_id>/unfollow')
def unfollow(user_id):
	user = User.query.filter_by(id=user_id).first()
	current_user.unfollow(user)
	return redirect(url_for('user.observe', user_id=user_id))
