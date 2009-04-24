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

import re
from datetime import datetime

from google.appengine.ext import webapp
from google.appengine.ext import db

from data.markup import Markup

register = webapp.template.create_template_register()

def markup(text):
	""" parses the markup string into HTML """
	return Markup.parse(text)

def humandate(stamp):
	""" parses the date into how long ago """
	difference = datetime.now() - stamp
	if (difference.days) > 0:
		result = str(difference.days) + " days ago..."
	elif (difference.seconds // 3600) > 1:
		result = str(difference.seconds // 3600) + " hours ago..."
	elif (difference.seconds // 60) > 1:
		result = str(difference.seconds // 60) + " minutes ago..."
	else:
		result = str(difference.seconds) + " seconds ago..."
	return result

def num(list):
	""" returns number of members in GQL list """
	return list.count()

register.filter(markup)
register.filter(humandate)
register.filter(num)