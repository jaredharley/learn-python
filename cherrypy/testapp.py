import os
import cherrypy

import sensor

class DisplayStatus(object):
	@cherrypy.expose
	def index(self):
		return open('testapp.html')

class StatusWebService(object):
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		print("inside GET def")
		return cherrypy.session['mystring']

	def POST(self):
		temp = sensor.ReadTempSensor()
		print(temp)
		return temp


if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
		},
		'/sensor': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public',
		},
	}

	webapp = DisplayStatus()
	webapp.sensor = StatusWebService()
	cherrypy.quickstart(webapp, '/', conf)