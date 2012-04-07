from google.appengine.ext import ndb

class Cellar(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    year = ndb.StringProperty()
    grapes = ndb.StringProperty()
    country = ndb.StringProperty()
    region = ndb.StringProperty()
    description = ndb.TextProperty()
    picture = ndb.StringProperty()

