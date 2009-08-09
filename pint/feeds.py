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
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from data.models import Account
from data.models import Message

class PersonnalFeed(webapp.RequestHandler):
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
		path = os.path.join(os.path.dirname(__file__), '../views/rss.xml')
		self.response.out.write(template.render(path, template_values))
        # I still haven't understood why we need to make the path...

class GeneralFeed(webapp.RequestHandler):
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


class FeedGen(webapp.RequestHandler):
	def get(self, params):

		params = re.sub('%2B', '+', params)

		self.response.headers['Content-Type'] = 'text/html'

		self.response.out.write('<h3>FeedGen for request "' + params + '"</h3>')

		userparams = re.search('user/([a-z+-]+)', params)
		if userparams:
			userparams = userparams.group(0)
			withusers = re.findall('(?:\+([a-z0-9]+))', userparams)
			withoutusers = re.findall('(?:-([a-z0-9]+))', userparams)

			self.response.out.write('<br/>&nbsp;With users: <b>' + '<b>&nbsp;</b>'.join(withusers) + '</b>')

			self.response.out.write('<br/>Without users: <b>' + '<b>&nbsp;</b>'.join(withoutusers) + '</b>')

		tagparams  = re.search('tag/([a-z+-]+)', params)
		if tagparams:
			tagparams = tagparams.group(0)
			withtags = re.findall('(?:\+([a-z0-9]+))', tagparams)
			withouttags = re.findall('(?:-([a-z0-9]+))', tagparams)

			self.response.out.write('<br/>With tags: <b>' + '<b>&nbsp;</b>'.join(withtags) + '</b>')

			self.response.out.write('<br/>Without tags: <b>' + '<b>&nbsp;</b>'.join(withouttags) + '</b>')
