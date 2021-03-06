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

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from data.models import Account

class Search(webapp.RequestHandler):
	def post(self):
		# Query: search & result list
		search = self.request.get('search')
		# Convert the search to lower case
		search = string.lower(search)
		results = list()
		# Make a loop to find results
		results_query = Account.all()
		for result in results_query:
			if string.lower(result.nickname) == search:
				results.append(result)
		
		# If there's no result 'not results' is True
		template_values = {
			'no_result': not results,
			'results': results
		}
		
		# We get the template path then show it
		path = os.path.join(os.path.dirname(__file__), '../views/search_result.html')
		self.response.out.write(template.render(path, template_values))