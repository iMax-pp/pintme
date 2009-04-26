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

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from data.models import Account
from data.models import LastFm

from libs.pylast import *

from data.vars   import __lastfmApiKey__
from data.vars   import __lastfmApiSecret__

class LastFmAuth(webapp.RequestHandler):
	def get(self):
		self.redirect('http://www.last.fm/api/auth/?api_key=' + __lastfmApiKey__)

class LastFmCallback(webapp.RequestHandler):
	def get(self):
		token = self.request.get('token')
		
		if token == '':
			self.redirect('/settings')

		user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", user.user_id()).get()

		sg = SessionKeyGenerator(__lastfmApiKey__, __lastfmApiSecret__)
		session_key = sg.get_web_auth_session_key_with_token(token)
		
		lastfm = LastFm()
		lastfm.sessionKey = session_key
		lastfm.put()
		
		account.lastFm = lastfm.key()
		account.put()
		
		authedUser = get_authenticated_user(__lastfmApiKey__, __lastfmApiSecret__, session_key)
		lastfm.userName = authedUser.get_name()
		lastfm.put()
		
		self.redirect('/settings')
