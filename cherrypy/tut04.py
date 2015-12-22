import random
import string
import cherrypy

class StringGenerator(object):
	@cherrypy.expose
	def index(self):
		return """<html>
			<head><title>Tutorial4</title></head>
			<body><form method="POST" action="generate">
			<input type="text" value="8" name="length" />
			<button type="submit">Generate</button>
			</form></body></html>"""

	@cherrypy.expose
	def generate(self, length=8):
		return ''.join(random.sample(string.hexdigits, int(length)))

if __name__ == '__main__':
	cherrypy.quickstart(StringGenerator())