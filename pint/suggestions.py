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
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Suggestion(db.Model):
	content = db.StringProperty(multiline=True)
	author = db.StringProperty()

class Suggestions(webapp.RequestHandler):
	def get(self):

		suggestions = Suggestion.all()

		template_data = {
			'suggestions': suggestions
		}
	
		path = os.path.join(os.path.dirname(__file__), '../views/suggestions.html')
		self.response.out.write(template.render(path, template_data))

	def post(self):
		suggestion = Suggestion()
	
		if users.get_current_user():
			user = users.get_current_user()
			suggestion.author = user.nickname()
		else:
			suggestion.author = "anon"
	
		suggestion.content = self.request.get('content')
		suggestion.put()
		
		self.redirect('/suggestions')