import cherrypy

config = {
	'server.socket_host': '0.0.0.0',
    'server.socket_port': 8001,
   }

class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True

cherrypy.config.update(config)
cherrypy.quickstart(HelloWorld())
