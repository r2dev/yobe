from .forms import RegisterationForm, LoginForm
from . import auth
from flask import request, redirect, url_for, flash, render_template
from flask.ext.login import login_required, current_user, current_user, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or render_template('index.html'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(render_template('index.html'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
			username=form.username.data,
			password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('A confirmation email has been sent to you by email') 
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)
