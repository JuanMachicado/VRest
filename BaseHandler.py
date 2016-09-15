import webapp2
import os
import jinja2
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_envAutoEscape = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_envAutoEscape.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        self.callback = self.request.get('callback')
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Credentials'] = 'true'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        self.response.headers['Access-Control-Max-Age'] = '3628800'
        if self.callback: 
            self.response.headers['Content-Type'] = 'text/javascript; charset=utf8'
        # else:
        #     self.response.headers['Content-Type'] = 'application/json; charset=utf8'
