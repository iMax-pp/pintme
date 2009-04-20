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

from site.models import Message
from site.models import Account

class MainPage(webapp.RequestHandler):
	def get(self):		
		# Default: last ten messages
		messages = Message.gql("ORDER BY date DESC LIMIT 10")
		
		# Declaration: following/followed lists
		followed_list = list()
		followers_list = list()
		
		# Query: is user logged in?
		user_status = "anon"
		user_nick = "unregistered"
		current_user = users.get_current_user()
		if current_user:
			# User Url = Logout
			log_url = users.create_logout_url(self.request.uri)
			user_status = "unregistered"
			
			# Query: is user registered?
			user_account = Account.gql("WHERE user = :1", current_user).get()
			user_nick = current_user.nickname()
			
            # User is registered!
			if user_account:
				user_status = "registered"
				
                # Query: Get the list of users being followed
				followed_list = Account.get(user_account.following)
				
                # Query: Get the list of the users followers
				followers_list = Account.gql("WHERE following = :1", user_account.key())
				
				# Default action (10 last messages), but only for the followed users
				user_account.following.append(user_account.key())
				messages = Message.gql("WHERE author IN :1 ORDER BY date DESC LIMIT 10", user_account.following)
		
		else:
			# Generate the login url
			log_url = users.create_login_url(self.request.uri)
	  	
		# Query: User is admin? (Could it be? Is the Savior here?)
		is_admin = users.is_current_user_admin()
       
		# Template values, yay!
		template_values = {
            'tab': "home",
            'messages': messages,
            'msg_num': messages.count(),
			'followed_list': followed_list,
			'followers_list': followers_list,
			'log_url': log_url,
			'user_status': user_status,
            'usernick': user_nick,
			'is_admin': is_admin,
            'composer_mode': self.request.get("mode","text")
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/index.html')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...