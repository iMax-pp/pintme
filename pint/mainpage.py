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
import re

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

from data.models import Account
from data.models import Message

class MainPage(webapp.RequestHandler):
	def get(self):		
	
		# Default declarations
		nickname = ''
		followed_list = list()
		followers_list = list()
		
		# Query: Get user login
		user = users.get_current_user()
		
		# User is logged in!
		if user:
			# Query: is user registered?
			account = Account.gql("WHERE userId = :1", user.user_id()).get()
			
            # User is registered!
			if account:
				nickname = account.nickname
				account.put()
				
                # Query: Get the list of users being followed
				followed_list = Account.get(account.following)
				
                # Query: Get the list of the users followers
				followers_list = Account.gql("WHERE following = :1", account.key())
				
				# I don't understand this line...
				# account.following.append(account.key())

				# Default action (10 last messages), but only for the followed users
				messages = Message.gql("WHERE author IN :1 ORDER BY date DESC LIMIT 10", account.following)
			else:
				# Default: last ten messages
				messages = Message.gql("ORDER BY date DESC LIMIT 10")
		
		else:
			# Default: last ten messages
			messages = Message.gql("ORDER BY date DESC LIMIT 10")
	  					
		# Template values, yay!
		template_values = {
            'tab': 'home',
            'messages': messages,
            'msg_num': messages.count(),
			'followed_list': followed_list,
			'followers_list': followers_list,
			'user': user,
            'nickname': nickname,
			'is_admin': users.is_current_user_admin(),
            'composer_mode': self.request.get("mode","text")
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/index.html')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...