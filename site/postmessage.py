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
from data.models import Message

# Do you think we could put all the actions in another file?
class PostMessage(webapp.RequestHandler):
	def post(self):
		# Declaration: new Message
		message = Message()
		
		# Query: user's Account & new message's content
		current_user = Account.gql("WHERE user = :1", users.get_current_user()).get()
		message.author = current_user.key()
		content = self.request.get('content')
		
		# And if the content isn't empty, off to the database! Happy message :D
		if content != '':
			message.content = content
			message.put()
	  
		self.redirect('/')