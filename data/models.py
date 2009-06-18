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

import random

from google.appengine.ext import db

class Image(db.Expando):
	name  = db.StringProperty()
	type  = db.StringProperty()
	data  = db.BlobProperty()
	mid   = db.BlobProperty()
	thumb = db.BlobProperty()

class LastFm(db.Model):
	userName = db.StringProperty()
	sessionKey = db.StringProperty()
	
class Account(db.Model):
	userId    = db.StringProperty()
	nickname  = db.StringProperty()
	avatar    = db.ReferenceProperty(Image)
	following = db.ListProperty(db.Key)
	lastFm    = db.ReferenceProperty(LastFm)
	regDate   = db.DateTimeProperty(auto_now_add=True)
	lastSeen  = db.DateTimeProperty(auto_now=True)

class Message(db.Model):
	author  = db.ReferenceProperty(Account)
	content = db.StringProperty(multiline=True)
	image   = db.ReferenceProperty(Image)
	link    = db.LinkProperty()
	date    = db.DateTimeProperty(auto_now_add=True)
	
class Token(db.Model):
	account = db.ReferenceProperty(Account)
	code     = db.StringProperty()
	expires = db.DateTimeProperty()
	
class Log(db.Model):
	data = db.StringProperty()
	time = db.DateTimeProperty(auto_now_add=True)
