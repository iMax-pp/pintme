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
from data.models import Image

from data.vars   import __lastfmApiKey__
from data.vars   import __lastfmApiSecret__

class AccountSettings(webapp.RequestHandler):
	def get(self):
		# Query: User's account
		user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", user.user_id()).get()
		
		if not account:
			self.redirect('/')
		else:
			# Query: User is admin?
			is_admin = users.is_current_user_admin()

			# Query: Get the list of the users followers
			followers_list = Account.gql("WHERE following = :1", account.key())

			# Last.fm account
			lastfmname = ''
			if account.lastFm != None:
				lastfmname = account.lastFm.userName
			
			# Template values
			template_values = {
				'tab': 'settings',
				'nickname': account.nickname,
				'user': user,
				'is_admin': is_admin,
				'lastfmname': lastfmname,
				'followed_list': Account.get(account.following),
				'followers_list': followers_list
			}
	
			# We get the template path then show it
			path = os.path.join(os.path.dirname(__file__), '../views/settings.html')
			self.response.out.write(template.render(path, template_values))

	def post(self):
		# Query: User's account & friend's nickname
		user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", user.user_id()).get()
		
		if(self.request.get('nickname')):		
			# Let's change the nickname
			# Query: nickname
			nickname = self.request.get('nickname')
			
			# Is the nickname available ?
			if nickname != account.nickname:
				nick_taken = Account.gql("WHERE nickname = :1", nickname).get()
				
				# Ok ? so change the nickname
				if not nick_taken:
					account.nickname = nickname
					account.put()
		
		if(self.request.get('avatar')):
			# Lets's change the avatar
			
			# Delete old avatar (garbage collector?)
			if account.avatar:
				account.avatar.delete()
				account.avatar = None
				
			# Store the image
			image = images.resize(self.request.get('avatar'), 100, 100)
			avatar = Image()
			avatar.data = db.Blob(image)
			avatar.put()
			
			# Update the user account
			account.avatar = avatar.key()
			account.put()

			# Update the memcache
			memcache.add('avatar'+account.nickname, account.avatar.data, 60)

		
		self.redirect('/settings')
