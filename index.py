#!/usr/bin/env python
#
# Copyright 2009 Simon&Humphries
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import os

from google.appengine.ext.webapp      import template
from google.appengine.api             import users
from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext             import db

from pint.mainpage    import MainPage
from pint.postmessage import PostMessage
from pint.profile     import Profile
from pint.register    import Register
from pint.settings    import AccountSettings
from pint.search	  import Search
from pint.connection  import Login
from pint.connection  import Logout
from pint.admin       import Admin
from pint.avatar      import Avatar
from pint.image       import GetImage
from pint.image       import MidImage
from pint.image       import Thumb
from pint.rss         import PersonnalRss
from pint.rss         import GeneralRss
from pint.lastfm      import LastFmAuth
from pint.lastfm      import LastFmCallback
from pint.about       import About
from pint.suggestions import Suggestions
from pint.maintenance import Maintenance

webapp.template.register_template_library('data.helpers')

application = webapp.WSGIApplication(
									 [('/', MainPage),
									  ('/compose', MainPage),
									  (r'/user/(.*)', Profile),
									  ('/post', PostMessage),
									  ('/register', Register),
									  (r'/account/(.*)/(.*)', AccountSettings),
									  ('/search', Search),
                                      ('/login', Login),
                                      ('/logout', Logout),
									  ('/admin', Admin),
                                      (r'/avatar/(.*)', Avatar),
                                      (r'/image/(.*)', GetImage),
                                      (r'/midimage/(.*)', MidImage),
                                      (r'/thumb/(.*)', Thumb),
                                      (r'/rss/personnal/(.*)', PersonnalRss),
                                      ('/rss/general', GeneralRss),
                                      ('/lastfmauth', LastFmAuth),
                                      (r'/lastfmcallback/.*', LastFmCallback),
									  ('/down', Maintenance),
									  ('/about', About),
                                      ('/suggestions', Suggestions)],
									 debug = True)

# Duh, it's the main!
def main():
	run_wsgi_app(application)

# And its friend, __main__ !
if __name__ == "__main__":
	main()
