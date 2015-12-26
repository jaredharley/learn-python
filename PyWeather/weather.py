import os, os.path
import urllib2
import json
import cherrypy

class Weather(object):
	@cherrypy.expose
	def index(self):
		return open('index.html')

	@cherrypy.expose
	def retrieveConditions(self, zip="20001"):
		# http://api.openweathermap.org/data/2.5/weather?zip=80917,us&APPID=5286470dfa5d5265f6ff06ebec2b4b98
		data = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?zip='+zip+',us&APPID=5286470dfa5d5265f6ff06ebec2b4b98'))
		temp = str(data[u'main'][u'temp'])
		return temp

	@cherrypy.expose
	def display(self):
		return cherrypy.session['myweather']

if __name__ == '__main__':
	cherrypy.quickstart(Weather(), '/', "app.conf")