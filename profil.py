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
from models import Message

class Profil(webapp.RequestHandler):
	def get(self, nickname):
		# Query: user's account & his 10th last messages
		if nickname == '':
			self.redirect('/')
		else:
			user = Account.gql("WHERE nickname = :1", nickname).get()
			if user == None:
				self.redirect('/')
			else:
				messages = Message.gql("WHERE author = :1", user.key()).fetch(10)
				followers_list = Account.gql("WHERE following = :1", user.key())
			
				# Query: Current user is admin?
				is_admin = users.is_current_user_admin()
				
				current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
				if nickname == current_user.nickname:
					self.redirect('/account_settings')
				
				else:
					# Template values
					template_values = {
						'user': user,
						'nickname': nickname,
						'messages': messages,
						'followed_list': Account.get(user.following),
						'followers_list': followers_list,
						'is_admin': is_admin
					}
					
					# We get the template path then show it
					path = os.path.join(os.path.dirname(__file__), 'profil.html')
					self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
									 [(r'/profil/(.*)', Profil)],
									 debug = True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
