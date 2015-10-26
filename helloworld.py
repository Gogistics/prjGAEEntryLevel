import webapp2, jinja2, os
from models import Log

# init models object
custom_index_log = Log()

JINJA_ENVIRONMENT = jinja2.Environment(
                    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
                    extensions = ['jinja2.ext.autoescape'],
                    autoescape = True)

# request handler
class MainPage(webapp2.RequestHandler):
    def get(self):
        # get user ip
        if self.request.remote_addr:
            custom_index_log.ip_address = self.request.remote_addr
            custom_index_log.put()

        # set template
        template = JINJA_ENVIRONMENT.get_template('index.html')
        
        # values to pass to front-end
        template_values = { 'title' : 'Bay Technology',
                            'greeting' : 'Hello Bay Tecnology'}
                            
        # dispatch template and values to front-end
        self.response.write(template.render(template_values))

# WSGI setting
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)