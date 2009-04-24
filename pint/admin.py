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

class Admin(webapp.RequestHandler):
	def get(self):

		current_user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", current_user.user_id()).get()
		
		newUsers = Account.gql("WHERE regDate > :1 ORDER BY regDate", account.lastSeen)

		account.put()
		
		# Template values, yay!
		template_values = {
			'tab': 'admin',
			'usernick': account.nickname,
			'is_admin': True,
			'newUserCount': newUsers.count(),
			'newUsers': newUsers
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/admin.html')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...