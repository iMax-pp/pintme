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
from google.appengine.ext import db

from data.models import Account
from data.models import Message

class Login(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect('/')
		else:
			self.redirect(users.create_login_url(self.request.uri))

class Logout(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			account = Account.gql("WHERE user = :1", user).get()
			account.put()
			self.redirect(users.create_logout_url(self.request.uri))
		else:
			self.redirect('/')