from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Jared'}
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