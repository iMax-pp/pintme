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
import random

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import MainTitle
from models import Message
from models import Account

class MainPage(webapp.RequestHandler):
	def get(self):		
		# By default we fetch the last ten messages
		message_query = Message.all().order('-date')
		messages = message_query.fetch(10)
		
		# An empty list of followed/ing friends (in case of an unsigned visitor)
		following = list()
		followed_by = list()
		
		# Check if user is logged in
		unknown_user = False
		if users.get_current_user():
			# Generate the logout url
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			anon = False

			# We check that the user is registered
			user_query = Account.all().filter('user = ', users.get_current_user())
			user_account = user_query.get()
			if user_account == None:
				unknown_user = True
			else:
				# If user exist we get his followed friends
				following = Account.get(user_account.following)
				# Followed by
				followed_by = Account.gql("WHERE following = :1", user_account.key())
				
				# And we fetch the last ten messages of him and his friends
				user_account.following.append(user_account.key())
				message_query = Message.gql("WHERE author IN :authors ORDER BY date DESC", authors = user_account.following)
				messages = message_query.fetch(10)
		
		else:
			# Generate the login url
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			anon = True
	  
		# Check if user is admin
		is_admin = users.is_current_user_admin()
		
		# Get random title
#		title_query = MainTitle.all()
#		titles = list()
#		for title in title_query:
#			titles.append(title)
#		random_title = random.choice(titles).title
		random_title = "<a>PINT</a>"
		
		# These values are to be sent to the template
		template_values = {
			'random_title': random_title,
			'unknown_user': unknown_user,
			'messages': messages,
			'following': following,
			'followed_by': followed_by,
			'url': url,
			'url_linktext': url_linktext,
			'anon': anon,
			'is_admin': is_admin
		}
	
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class PostMessage(webapp.RequestHandler):
	def post(self):
		# Set up the message instance
		message = Message()
		# A Reference to the current user
		user = Account.gql("WHERE user = :user", user=users.get_current_user())
		for current_user in user:
			message.author = current_user.key()
		
		# And if the content isn't empty we put all in the db
		if self.request.get('content') != '':
			message.content = self.request.get('content')
			message.put()
	  
		self.redirect('/')

class NewUser(webapp.RequestHandler):
	def post(self):
		new_user = Account()
		
		accounts = Account.all()
		accounts.filter('nickname = ', self.request.get('nickname'))
		nick_already_exist = accounts.get()
		
		if nick_already_exist == None:
			new_user.user = users.get_current_user()
			new_user.nickname = self.request.get('nickname')
			new_user.put()
		
		self.redirect('/')

application = webapp.WSGIApplication(
									 [('/', MainPage),
									  ('/index.*', MainPage),
									  ('/post', PostMessage),
									  ('/register', NewUser)],
									 debug = True)


def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
