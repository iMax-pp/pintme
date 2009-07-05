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
import string
import random

from datetime import datetime, timedelta

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

from pintcore.useraccount import UserAccount

from data.models import Account
from data.models import Message

class Profile(webapp.RequestHandler):
	def get(self, nickname):

		if nickname == '':

			self.redirect('/')

		else:

			profile = UserAccount()
			profile.getFromNickname( nickname )

			# Called user doesn't exist
			if not profile.validAccount:

				self.redirect('/')

			else:

				user = UserAccount()
				user.getFromSession()

				'''if isOwner:
					token = Token()
					token.account = account.key()
					avatar_token  = string.join( random.sample( string.letters + string.digits, 30  ), '' )
					token.code    = avatar_token
					expires = datetime.now() + timedelta( hours = 1 )
					token.expires = expires
					token.put()
				else:
					avatar_token = '' '''


				# Template values
				template_values = {
					'user': user.account,
					'profile': profile.account,
					'canFollow': user.canFollow( profile ),
					'profileMessages': profile.getSentMessages(),
					'profileFollowed': profile.getFollowed(),
					'profileFollowers': profile.getFollowers()
				}

				# We get the template path then show it
				path = os.path.join(os.path.dirname(__file__), '../views/profile.html')
				self.response.out.write(template.render(path, template_values))

	def post(self, follow_nick):
		# Toggle following a user or not
		# Query: User's account & friend's nickname

		current_user = users.get_current_user()
		account = Account.gql("WHERE userId = :1", current_user.user_id()).get()

		# Does that user exist?
		follow_account = Account.gql("WHERE nickname = :1", follow_nick).get()
		if follow_account != None:
			if follow_account.key() in account.following:
				account.following.remove(follow_account.key())
			else:
				account.following.append(follow_account.key())
			account.put()

		self.redirect('/user/'+follow_nick)
