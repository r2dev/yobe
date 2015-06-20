
from flask import render_template, url_for, redirect
from flask.ext.login import current_user
from ..models import Post
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
	posts = Post.query.filter_by(author_id=current_user.id).order_by(
		Post.timestamp.desc())
	return render_template('index.html', form=form, posts=posts)