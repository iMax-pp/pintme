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

from datetime import datetime

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from data.models import Account
from data.models import Image
from data.models import Token
from data.models import Log

from data.vars   import __lastfmApiKey__
from data.vars   import __lastfmApiSecret__

class AccountSettings(webapp.RequestHandler):
	def post(self, type, token_code):

		'''
			This is where our Flash uploader sends the data
			As Flash doesn't care about cookies or sessions,
			we have to send a token to authentificate...
		'''

		log = Log()

		token = Token.gql("WHERE code = :1", token_code ).get()
		
		if token:
			if token.expires > datetime.now():

				account = token.account
				
				if account.avatar:
				  account.avatar.delete()
				  account.avatar = None

				data = self.request.get('Filedata')
						
				image = images.resize(data, 100, 100)
				avatar = Image()
				avatar.data = db.Blob( image )
				avatar.put()
				
				account.avatar = avatar.key()
				account.put()

				# Update the memcache
				memcache.add('avatar'+account.nickname, account.avatar.data, 60)
				
				log.data = 'Valid Token, avatar changed.'

			else:
				log.data = 'Token expired'
		else:
			log.data = 'No such token'
			
		log.put()
		
		print 'Content-Type: text/plain'
		print ''
		print 'Hello, world!'