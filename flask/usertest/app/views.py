from app import app, db, lm

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .decorators import required_roles
from .forms import LoginForm
from .models import User
from datetime import datetime

#import pdb; pdb.set_trace() <-- put at line to create breakpoint

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	#if g.user.is_authenticated:
	#	g.user.last_seen = datetime.utcnow()
	#	db.session.add(g.user)
	#	db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.emailAddress.data).first()
		if user is not None and user.passwordValid(form.password.data):
			if login_user(user):
				flash('Logged in successfully','success')
				user.last_logon = datetime.utcnow()
				db.session.add(user)
				db.session.commit()
				return redirect(url_for('protected'))
			else:
				flash('This user is disabled')
		else:
			flash('invalid username or password','danger')
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/test')
@required_roles('admin')
def test(self):
	return "You have permission to see this page."

@app.route('/protected')
@login_required
def protected():
	return "You logged in"