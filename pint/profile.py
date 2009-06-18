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
import string
import random

from datetime import datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from libs.pylast import *

from data.models import Account
from data.models import Message
from data.models import Token
from data.vars import *

from data.vars   import __lastfmApiKey__
from data.vars   import __lastfmApiSecret__

class Profile(webapp.RequestHandler):
	def get(self, nickname):
		if nickname == '':
			self.redirect('/')
		else:
			# Get the users account using nickname
			called_user = Account.gql("WHERE nickname = :1", nickname).get()
			
			# Called user doesn't exist
			if called_user == None:
				self.redirect('/')
			else:

				''' This is the profile data '''
				
				# Users last 10 messages
				messages = Message.gql("WHERE author = :1 ORDER BY date DESC LIMIT 10", called_user.key()).fetch(10)

				# Users followers
				followers_list = Account.gql("WHERE following = :1", called_user.key())
				followed_list = Account.get(called_user.following)
				if len(followed_list) == 0:
					followed_list = None


				''' This is the viewer data '''

				# Get viewers account (could be unregistered)
				current_user = users.get_current_user()

				if current_user:
					account = Account.gql("WHERE userId = :1", current_user.user_id()).get()
					account.put()

					nickname = account.nickname

					# The follow/unfollow button
					follow = ''
					if account != None:
						if called_user.key() not in account.following:
							follow = 'possible'
						else:
							follow = 'unfollow'
				
					# Is this the users profile?
					isOwner = ( nickname == account.nickname )
					
					if isOwner:
						token = Token()
						token.account = account.key()
						avatar_token  = string.join( random.sample( string.letters + string.digits, 30  ), '' )
						token.code    = avatar_token
						expires = datetime.now() + timedelta( hours = 1 )
						token.expires = expires
						token.put()
					else:
						avatar_token = ''
						
				else:
					nickname = ''
					avatar_token = ''
					follow = ''
			

				# Template values
				template_values = {
					'tab': 'profile',
					'nickname': nickname,
					'user': current_user,
					'avatar_token': avatar_token,
					'is_admin': users.is_current_user_admin(),
					'called_user': called_user,
					'follow': follow,
					'messages': messages,
					'followed_list': followed_list,
					'followers_list': followers_list
				}

				# We get the template path then show it
				path = os.path.join(os.path.dirname(__file__), '../views/profile.html')
				self.response.out.write(template.render(path, template_values))

	def post(self, follow_nick):
		# Toggle following a user or not
		# Query: User's account & friend's nickname

		current_user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", current_user.user_id()).get()
		
		# Does that user exist?
		follow_account = Account.gql("WHERE nickname = :1", follow_nick).get()
		if follow_account != None:
			if follow_account.key() in account.following:
				account.following.remove(follow_account.key())
			else:
				account.following.append(follow_account.key())
			account.put()
		
		self.redirect('/user/'+follow_nick)