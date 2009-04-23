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

class NewUser(webapp.RequestHandler):
	def post(self):
		# Declaration: new Account
		# Query: nickname
		new_user = Account()
		nickname = self.request.get('nickname')
		
		# Query: Is nickname already exist ?
		nick_already_exist = Account.gql("WHERE nickname = :1", nickname).get()
		
		# If not let's create the new user !
		if nick_already_exist == None:
			new_user.user = users.get_current_user()
			new_user.nickname = nickname
			new_user.put()
		
		self.redirect('/')