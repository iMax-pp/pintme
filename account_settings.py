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
		# Query: User's account
		current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
		
		if not current_user:
			self.redirect('/')
		else:
			# Query: User is admin?
			is_admin = users.is_current_user_admin()
	
			# Query: Get the list of the users followers
			followers_list = Account.gql("WHERE following = :1", current_user.key())
			
			# Template values
			template_values = {
				'current_user': current_user,
				'followed_list': Account.get(current_user.following),
				'followers_list': followers_list,
				'is_admin': is_admin
			}
	
			# We get the template path then show it
			path = os.path.join(os.path.dirname(__file__), 'account_settings.html')
			self.response.out.write(template.render(path, template_values))

class PostSettings(webapp.RequestHandler):
	def post(self):
		# Query: User's account & friend's nickname
		current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
		
		# Let's change the nickname
		# Query: nickname
		nickname = self.request.get('nickname')
		
		# Is the nickname available ?
		if nickname != current_user.nickname:
			nick_already_exist = Account.gql("WHERE nickname = :1", nickname).get()
			
			# Ok ? so change the nickname
			if nick_already_exist == None:
				current_user.nickname = nickname
				current_user.put()
		
		self.redirect('/account_settings')


application = webapp.WSGIApplication(
									 [('/account_settings', AccountSettings),
									  ('/account_settings/post', PostSettings)],
									 debug = True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
