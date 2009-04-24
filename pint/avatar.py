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
from google.appengine.api import memcache

from data.models import Account
from data.models import Image

class Avatar(webapp.RequestHandler):
	
	def get(self, nickname):
		
		# Get the users account using nickname
		called_user = Account.gql("WHERE nickname = :1", nickname).get()
		
		if called_user:						
			if called_user.avatar:
				self.response.headers['Content-Type'] = "image/jpg"
				data = memcache.get('avatar'+nickname)
				if data is None:
					data = called_user.avatar.data
					memcache.add('avatar'+nickname, data, 60)
				self.response.out.write(data)
				  
			else:
				self.response.headers['Content-Type'] = "image/gif"
				self.response.out.write(open('zoid.gif','rb').read())
		else:
			self.response.headers['Content-Type'] = "image/gif"
			self.response.out.write(open('zoid.gif','rb').read())
