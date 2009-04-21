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

from data.models import Account
from data.models import Message

class Profile(webapp.RequestHandler):
	def get(self, nickname):
		# Query: user's account & his 10th last messages
		if nickname == '':
			self.redirect('/')
		else:
			current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
			if current_user == None:
				self.redirect('/')
			else:
				if nickname == current_user.nickname:
					self.redirect('/settings')
				else:
					user = Account.gql("WHERE nickname = :1", nickname).get()
					if user == None:
						self.redirect('/')
					else:
						follow_him = (current_user != None)
						if follow_him:
							follow_him = user.key() not in current_user.following
						messages = Message.gql("WHERE author = :1", user.key()).fetch(10)
						followers_list = Account.gql("WHERE following = :1", user.key())
					
						# Query: Current user is admin?
						is_admin = users.is_current_user_admin()
					
						# Template values
						template_values = {
							'user': user,
							'follow_him': follow_him,
							'nickname': nickname,
							'messages': messages,
							'followed_list': Account.get(user.following),
							'followers_list': followers_list,
							'is_admin': is_admin
						}
					
						# We get the template path then show it
						path = os.path.join(os.path.dirname(__file__), '../views/profile.html')
						self.response.out.write(template.render(path, template_values))

	def post(self):
		# Let's adding a Friend to following list
		# Query: User's account & friend's nickname
		current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
		friend_added = self.request.get('friend_added')
		
		# And if he exists, isn't the user himself and isn't already in the list, let's add it to the list
		friend_account = Account.gql("WHERE nickname = :1", friend_added).get()
		if friend_account != None:
			current_user.following.append(friend_account.key())
			current_user.put()
		
		self.redirect('/')