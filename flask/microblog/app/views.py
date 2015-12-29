from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import EditForm
from .models import User
from oauth import OAuthSignIn
from datetime import datetime

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	# Array of example posts
	posts = [
		{
			'author': {'nickname': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'nickname': 'Adam'},
			'body': 'Star Wars was so cool.'
		}
	]
	return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	return render_template('login.html',
						   title='Sign in')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email = oauth.callback()
	if social_id is None:
		flash('Authentication failed')
		return redirect(url_for('index'))
	user = User.query.filter_by(social_id=social_id).first()
	if not user:
		user = User(social_id=social_id, nickname=username, email=email)
		db.session.add(user)
		db.session.commit()
	login_user(user, True)
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User \'%s\' was not found.' % nickname)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		g.user.email    = form.email.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
		form.email.data	   = g.user.email
	return render_template('edit.html', form=form)