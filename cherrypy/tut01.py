import cherrypy

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return "Hello there, world!"

if __name__ == '__main__':
	cherrypy.quickstart(HelloWorld())