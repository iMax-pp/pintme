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

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

from data.models import Image

class GetImage(webapp.RequestHandler):
	
	def get(self, name):
		
		data = memcache.get('img' + name)
		if data:
			imagetype = imghdr.what(file, data)
		else:
			image = Image.gql("WHERE name = :1", name).get()
			imagetype = image.type
			data = image.data
		
		if data:						  
			memcache.add('img' + name, data, 60)
			if imagetype == 'jpeg':
				self.response.headers['Content-Type'] = "image/jpg"
			elif imagetype == 'gif':
				self.response.headers['Content-Type'] = "image/gif"
			elif imagetype == 'png':
				self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(data)
		else:
			self.response.headers['Content-Type'] = "image/gif"
			self.response.out.write(open('zoid.gif','rb').read())

class MidImage(webapp.RequestHandler):
	
	def get(self, name):

		data = memcache.get('mid' + name)
		if data:
			imagetype = imghdr.what(file, data)
		else:
			image = Image.gql("WHERE name = :1", name).get()
			imagetype = image.type
			data = image.mid
		
		if data:						  
			memcache.add('mid' + name, data, 60)
			if imagetype == 'jpeg':
				self.response.headers['Content-Type'] = "image/jpg"
			elif imagetype == 'gif':
				self.response.headers['Content-Type'] = "image/gif"
			elif imagetype == 'png':
				self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(data)
		else:
			self.response.headers['Content-Type'] = "image/gif"
			self.response.out.write(open('zoid.gif','rb').read())

class Thumb(webapp.RequestHandler):
	
	def get(self, name):

		data = memcache.get('thumb' + name)
		if data:
			imagetype = imghdr.what(file, data)
		else:
			image = Image.gql("WHERE name = :1", name).get()
			imagetype = image.type
			data = image.thumb
		
		if data:						  
			memcache.add('thumb' + name, data, 60)
			if imagetype == 'jpeg':
				self.response.headers['Content-Type'] = "image/jpg"
			elif imagetype == 'gif':
				self.response.headers['Content-Type'] = "image/gif"
			elif imagetype == 'png':
				self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(data)
		else:
			self.response.headers['Content-Type'] = "image/gif"
			self.response.out.write(open('zoid.gif','rb').read())
