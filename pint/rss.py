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

class PersonnalRss(webapp.RequestHandler):
	def get(self, nickname):
		
		account = Account.gql("WHERE nickname = :1", nickname).get()
		messages = Message.gql("WHERE author IN :1 ORDER BY date DESC LIMIT 10", account.following)
		
		template_values = {
			'title': nickname + '\'s feed',
			'link': 'http://pintme.appspot.com/user/' + nickname,
			'description': 'Personnal user feed for ' + nickname,
			'items': messages
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/rss.html')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...
		
class GeneralRss(webapp.RequestHandler):
	def get(self):
		
		messages = Message.gql("ORDER BY date DESC LIMIT 30")
		
		template_values = {
			'title': 'PintMe General Feed',
			'link': 'http://pintme.appspot.com/',
			'description': 'PintMe General Feed',
			'items': messages
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/rss.html')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...