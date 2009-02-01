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

from models import Message
from models import Account

class MainPage(webapp.RequestHandler):
	def get(self):
		# We fetch all the accounts
		authors = Account.all()
		
		# We fetch the last ten messages
		message_query = Message.all().order('-date')
		messages = message_query.fetch(10)
		
		# Check if user is logged in
		unknown_user = False
		if users.get_current_user():
			# Generate the logout url
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			anon = False

			# We check that the user is registered
			accounts = Account.all()
			accounts.filter('user = ', users.get_current_user())
			account = accounts.get()
			if account == None:
				unknown_user = True
		else:
			# Generate the login url
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			anon = True
	  
		# Check if user is admin
		is_admin = users.is_current_user_admin()
	    
		# Choose a random title
   		titles = ('<a>PINT</a>Spot', '<a>PINT</a>ed', '<a>PINT</a>Me', '<a>PINT</a>Soft', '<a>PINT</a>Hard', '<a>PINT</a>SM', '<a>PINT</a>ware', '<a>PINT</a>BDSM', '<a>PINT</a>BSD', '<a>PINT</a>LSD', '<a>PINT</a>ou (or ubuntu)', '<a>PINT</a>ubuntu', 'i<a>PINT</a>', 'you<a>PINT</a>', 'Google <a>PINT</a>', '<a>PINT</a>Please', '<a>PINT</a>Sorry', '<a>PINT</a>Welcomed', '<a>PINT</a>Again', '<a>PINT</a>guin', 'JustOne<a>PINT</a>', 'JustAnother<a>PINT</a>', 'OneMore<a>PINT</a>', 'Bier&<a>PINT</a>', '<a>PINT</a>OfVodka', '<a>PINT</a>ade', '<a>PINT</a>aid', '<a>PINT</a>ADD', '<a>PINT</a>INC', '<a>PINT</a>agramme', '<a>PINT</a>-A-Gramme', '<a>PINT</a>-A-Kilo', 'Pound-A-<a>PINT</a>', 'Fish<a>PINT</a>', '<a>PINT</a>Sized', 'Mystic<a>PINT</a>', 'Super<a>PINT</a>', 'Hyper<a>PINT</a>', 'Quantic<a>PINT</a>', 'QuantumOf<a>PINT</a>', 'Electro<a>PINT</a>', 'Royal<a>PINT</a>', 'Republican<a>PINT</a>', 'YesWeCan...<a>PINT</a>', 'WhatTheFucking...<a>PINT</a>', 'IVotedFor<a>PINT</a>', 'WhatSThe<a>PINT</a>', '<a>PINT</a>Aday', '<a>PINT</a>IsMine', 'my<a>PINT</a>!', '<a>PINT</a>Book', '<a>PINT</a>Book-Air', 'less Air, more <a>PINT</a>', 'Apple<a>PINT</a>', 'Web<a>PINT</a>', 'Command+<a>PINT</a>', 'Ctrl+Meta+Alt+<a>PINT</a>', ':<a>PINT</a>', '3Click<a>PINT</a>', 'Black<a>PINT</a>', '<a>PINT</a>sh', '<a>PINT</a> (<a>PINT</a> Is Not Twilight)', 'tinP', 'tniP', 'Tonight<a>PINT</a>', 'Coffee<a>PINT</a>', 'Breakfast<a>PINT</a>', 'Bacon<a>PINT</a>', '<a>PINT</a>Pause', '<a>PINT</a>-nic', '<a>PINT</a>Address', '<a>PINT</a>Phone', 'Multi<a>PINT</a>', 'Simple<a>PINT</a>...', 'FourFingers<a>PINT</a>', 'Start<a>PINT</a>', 'Stop<a>PINT</a>', '<a>PINT</a>', '<a>PINT</a>EGER', 'FloatOr<a>PINT</a>', '<a>PINT</a>Pointer', 'Master<a>PINT</a>er', 'License<a>PINT</a>er', 'GNU<a>PINT</a>', '<a>PINT</a>ix', '<a>PINT</a>ux', '<a>PINT</a>ium', '<a>PINT</a>OS', 'ThanksForThe<a>PINT</a>', 'LordOfThe<a>PINT</a>', 'Piss<a>PINT</a>', '<a>PINT</a>8', '666 Number Of The <a>PINT</a>', 'Bug<a>PINT</a>', 'BlueScreenOf<a>PINT</a>', '<a>PINT</a>Panic', '<a>PINT</a>OSleep', '<a>PINT</a>craft', 'War<a>PINT</a>', '<a>PINT</a>OfDead', '<a>PINT</a>sOfTheCaribeans', 'TheLast<a>PINT</a>', '<a>PINT</a>:Revolution', '<a>PINT</a>:Resurrection', 'Evil<a>PINT</a>', 'TheIncredible<a>PINT</a> ', 'X<a>PINT</a> ', 'Y<a>PINT</a>', 'Why<a>PINT</a>', 'Inexhaustible<a>PINT</a>', 'SauronS<a>PINT</a>', 'Sleepy<a>PINT</a>', 'NeverSleep<a>PINT</a>', '<a>PINT</a>Wars', 'P1N7')
		random_title = random.choice(titles)
		
		# These values are to be sent to the template
		template_values = {
			'random_title': random_title,
			'unknown_user': unknown_user,
			'messages': messages,
			'authors': authors,
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
		
		message.author = users.get_current_user()
		
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
									  ('/post', PostMessage),
									  ('/register', NewUser)],
									 debug = True)


def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
