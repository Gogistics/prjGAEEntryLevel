import webapp2, jinja2, os, json, urllib, urllib2
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
            # query geo-location of IP
            query_args = { 'token' : 'dWEF43tHwFfgG51ASeFg5087rtRBR', 'ip' : self.request.remote_addr }
            encoded_args = urllib.urlencode(query_args)
            url = 'http://52.34.94.166:3000/get_ip_geo'
            result = json.loads(urllib2.urlopen(url, encoded_args).read())
            lat_lng = result['geo']['ll']
            
            # store data
            custom_index_log.ip_address = self.request.remote_addr
            custom_index_log.lat = lat_lng[0].__str__()
            custom_index_log.lng = lat_lng[1].__str__()
            custom_index_log.put()

        # set template
        template = JINJA_ENVIRONMENT.get_template('index.html')
        
        # get ip addresses of visitors
        ip_logs = Log.query().order(-Log.access_time)
        
        # values to pass to front-end
        template_values = { 'title' : 'Bay Technology',
                            'greeting' : 'Hello Bay Tecnology',
                            'ip_logs' : ip_logs}
                            
        # dispatch template and values to front-end
        self.response.write(template.render(template_values))

# WSGI setting
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)