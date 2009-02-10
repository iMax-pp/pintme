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

from models import Account

class AccountSettings(webapp.RequestHandler):
	def get(self):
		# If user isn't log in we redirect him to the main page
		if not users.get_current_user():
			self.redirect('/')
		else:
			# Get the user account 
			user_account = Account.gql("WHERE user = :1", users.get_current_user()).get()
		
			# Check if user is admin
			is_admin = users.is_current_user_admin()
		
			# Followed by
			followers_list = Account.gql("WHERE following = :1", user_account.key())
				
			# These values are to be sent to the template
			template_values = {
				'user_account': user_account,
				'followed_list': Account.get(user_account.following),
				'followers_list': followers_list,
				'is_admin': is_admin
			}
		
			# We get the template path then show it
			path = os.path.join(os.path.dirname(__file__), 'account_settings.html')
			self.response.out.write(template.render(path, template_values))

class PostSettings(webapp.RequestHandler):
	def post(self):
		# Get the user account
		user_account = Account.gql("WHERE user = :1", users.get_current_user()).get()
		
		# Add a friend
		friend_added = self.request.get('friend_added')
		if friend_added != '':
			accounts = Account.all()
			for user in accounts:
				if friend_added == user.nickname:
					# Verify not already in the list and do it
					if (user.key() not in user_account.following) & (friend_added != user_account.nickname):
						user_account.following.append(user.key())
						user_account.put()
					break
		
		if self.request.get('nickname') != user_account.nickname:
			nick_already_exist = Account.gql("WHERE nickname = :1", self.request.get('nickname')).get()

			if nick_already_exist == None:
				new_user.nickname = self.request.get('nickname')
				new_user.put()
		
		self.redirect('/account_settings')

application = webapp.WSGIApplication(
									 [('/account_settings', AccountSettings),
									  ('/account_settings/post', PostSettings)],
									 debug = True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

