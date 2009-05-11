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
import imghdr 
import re

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from data.models import Account
from data.models import Message
from data.models import Image

# Do you think we could put all the actions in another file?
class PostMessage(webapp.RequestHandler):
	def post(self):
		
		if self.request.get('textmessage') != '':

			message = Message()
			
			# Query: user's Account & new message's content
			current_user = users.get_current_user()
			account = Account.gql("WHERE userId = :1", current_user.user_id()).get()
			message.author = account.key()
	
			content = self.request.get('textmessage')
			
			# And if the content isn't empty, off to the database! Happy message :D
			if content != '':
				message.content = content
				message.put()
				
			self.redirect('/')
			
			
		imagedata = self.request.get('imageupload')
		if imagedata != '':

			current_user = users.get_current_user()
			account = Account.gql("WHERE userId = :1", current_user.user_id()).get()
				
			filename = self.request.body_file.vars['imageupload'].filename
			filename = re.sub(r' ', r'_', filename)
			imagetype = imghdr.what(file,imagedata)
			middata = images.resize(imagedata, 300, 300)
			thumbdata = images.resize(imagedata, 100, 100)
	
			image = Image()
			image.name = filename
			image.type = imagetype
			image.data = db.Blob(imagedata)
			image.mid = db.Blob(middata)
			image.thumb = db.Blob(thumbdata)
			image.put()

			# Update the memcache
			memcache.add('img' + filename, imagedata, 60)
			memcache.add('mid' + filename, middata, 60)
			memcache.add('thumb' + filename, thumbdata, 60)

			message = Message()
			message.author = account.key()
			message.content = self.request.get('imgdesc')
			message.image = image.key()
			message.put()
			
		self.redirect('/')