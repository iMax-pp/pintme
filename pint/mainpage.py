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
from google.appengine.ext import webapp

from pintcore.useraccount import UserAccount

from data.models import Account
from data.models import Message

class MainPage(webapp.RequestHandler):
	def get(self):

		user = UserAccount()
		user.getFromSession()

		# Template values, yay!
		if user.validAccount:
			template_values = {
				'messages': user.getMessages(),
				'nickname': user.account.nickname
			}
		else:
			template_values = {
				'messages': None,
				'nickname': ''
			}

		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/index.html')
		self.response.out.write(template.render(path, template_values))
