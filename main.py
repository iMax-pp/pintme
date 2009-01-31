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
	    
		# Un titre au hasard a chaque coup
   		titles = ('PintSpot', 'Pinted', 'PintMe', 'PintSoft', 'PintHard', 'PintSM', 'Pintware', 'PintBDSM', 'PintBSD', 'PintLSD', 'Pintou (or ubuntu)', 'Pintubuntu', 'iPint', 'youPint', 'Google Pint', 'PintPlease', 'PintSorry', 'PintWelcomed', 'PintAgain', 'Pintguin', 'JustOnePint', 'JustAnotherPint', 'OneMorePint', 'Bier&Pint', 'PintOfVodka', 'Pintade', 'Pintaid', 'PintADD', 'PintINC', 'Pintagramme', 'Pint-A-Gramme', 'Pint-A-Kilo', 'Pound-A-Pint', 'FishPint', 'PintSized', 'MysticPint', 'SuperPint', 'HyperPint', 'QuanticPint', 'QuantumOfPint', 'ElectroPint', 'RoyalPint', 'RepublicanPint', 'YesWeCan...Pint', 'WhatTheFucking...Pint', 'IVotedForPint', 'WhatSThePint', 'PintAday', 'PintIsMine', 'myPint!', 'PintBook', 'PintBook-Air', 'less Air, more Pint', 'ApplePint', 'WebPint', 'Command+Pint', 'Ctrl+Meta+Alt+Pint', ':pint', '3ClickPint', 'BlackPint', 'Pintsh', 'Pint (Pint Is Not Twilight)', 'tinP', 'tniP', 'TonightPint', 'CoffeePint', 'BreakfastPint', 'BaconPint', 'PintPause', 'Pint-nic', 'PintAddress', 'PintPhone', 'MultiPint', 'SimplePint...', 'FourFingersPint', 'StartPint', 'StopPint', 'pINT', 'pINTEGER', 'FloatOrPint', 'PintPointer', 'MasterPinter', 'LicensePinter', 'GNUPint', 'Pintix', 'Pintux', 'Pintium', 'PintOS', 'ThanksForThePint', 'LordOfThePint', 'PissPint', 'Pint8', '666 Number Of The Pint', 'BugPint', 'BlueScreenOfPint', 'PintPanic', 'PintOSleep', 'Pintcraft', 'WarPint', 'PintOfDead', 'PintsOfTheCaribeans', 'TheLastPint', 'Pint:Revolution', 'Pint:Resurrection', 'EvilPint', 'TheIncrediblePint ', 'XPint ', 'YPint', 'WhyPint', 'InexhaustiblePint', 'SauronSPint', 'SleepyPint', 'NeverSleepPint')
		subtitle = random.choice(titles)
		# These values are to be sent to the template
		template_values = {
			'subtitle': subtitle,
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
