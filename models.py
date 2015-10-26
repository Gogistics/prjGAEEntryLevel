from google.appengine.ext import ndb

class Log(ndb.Model):
    access_time = ndb.DateTimeProperty(auto_now_add=True)
    ip_address = ndb.StringProperty()