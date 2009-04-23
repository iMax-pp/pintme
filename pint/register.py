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

class Register(webapp.RequestHandler):
	def get(self):
		# This is the first registration page, just the pseudonym, nothing more
		
		template_data = {
            'tab': 'onemorething',
			'nickname': '',
            'user': users.get_current_user(),
			'is_admin': users.is_current_user_admin()
		}
		
		path = os.path.join(os.path.dirname(__file__), '../views/register.html')
		self.response.out.write(template.render(path, template_data))
		
	def post(self):
		# Declaration: new Account
		# Query: nickname
		new_user = Account()
		nickname = self.request.get('nickname')
		
		if len(nickname) < 3:
			self.redirect('/register')
		
		# Query: nickname taken ?
		nick_taken = Account.gql("WHERE nickname = :1", nickname).get()

		if nick_taken:
			self.redirect('/register')
		
		else:
			# If not let's create the new user !
			new_user.userId = users.get_current_user().user_id()
			new_user.nickname = nickname
			new_user.put()
			
			self.redirect('/')