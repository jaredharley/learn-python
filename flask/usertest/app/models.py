from app import bcrypt, db
from flask.ext.login import UserMixin
from hashlib import md5
from datetime import datetime

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String)
	active = db.Column(db.Boolean, nullable=False, default=True)
	last_logon = db.Column(db.DateTime)
	created = db.Column(db.DateTime, default=datetime.utcnow)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return self.active
	
	@property
	def is_anonymous(self):
		return False
	
	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def passwordValid(self, testPassword):
		if bcrypt.check_password_hash(self.password, testPassword):
			print self.email + 'entered valid credentials.'
			return True
		else:
			print self.email + ' entered invalid credentials.'
			return False

	def avatar(self, size):
		avatarhash = md5(self.nickname.encode('utf-8')).hexdigest()
		return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (avatarhash, size)

	def __repr__(self):
		return '<User %r>' % (self.email)