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
from google.appengine.ext import webapp

class Markup:
	@classmethod
	def paragraphs(cls, text):
		text = text + '\n'
		text = re.sub(r'\n+', r'\n', text)
		return re.sub(r'([^\n]+)\n', r'<p>\1</p>', text)
		
	@classmethod
	def bold(cls, text):
		return re.sub(r'\*([^\*]*)\*', r'<b>\1</b>', text)

	@classmethod
	def italic(cls, text):
		return re.sub(r'_([^\_]*)_', r'<i>\1</i>', text)
	
	@classmethod
	def verbatim(cls, text):
		# FIXME This only works with a single line.
		# 		( With more, only the first one is verbatimized :)
		return re.sub(r'\{\{\{(.*\n*)\}\}\}', r'<code>\1</code>', text)
	
	@classmethod
	def hline(cls, text):
		return re.sub(r'\-\-[\-]+', r'<hr/>', text)
	
	@classmethod
	def smileys(cls, text):
		text = re.sub(r'\s:[\-]?\)\s', ' <b class="smiley">:)</b> ', text)
		text = re.sub(r'\s:[\-]?[dD]\s', ' <b class="smiley">:D</b> ', text)
		text = re.sub(r'\s;[\-]?\)\s', ' <b class="smiley">;)</b> ', text)
		text = re.sub(r'\s:\'[\-]?\(\s', ' <b class="smiley">:\'(</b> ', text)
		text = re.sub(r'\s:[\-]?[oO]\s', ' <b class="smiley">:-o</b> ', text)
		text = re.sub(r'\s:[\-]?[\\\/]\s', ' <b class="smiley">:-/</b> ', text)
		text = re.sub(r'\s[xX][\-]?\(\s', ' <b class="smiley">x-(</b> ', text)
		text = re.sub(r'\s:[\-]?\(\s', ' <b class="smiley">:(</b> ', text)
		text = re.sub(r'\s[8bB][\-]?\)\s', ' <b class="smiley">B-)</b> ', text)
		text = re.sub(r'\s:[\-]?[pP]\s', ' <b class="smiley">:P</b> ', text)
		text = re.sub(r'\s\<3\s', ' <b class="smiley"><3</b> ', text)
		text = re.sub(r'\s:[\-]?\|\s', ' <b class="smiley">:-|</b> ', text)
		return text
	
	@classmethod
	def urls(cls, text):
		text = re.sub(r'((?:udp|smtp|pop3|ssh|telnet|https?|s?ftp|imap|git|cvs|svn)://(?:[a-z0-9-]+\.)*[a-z0-9]+\.(?:aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|co\.uk|gouv\.fr|[a-z]{2})(?:\:[0-9]{1,6})?(?:/[a-z0-9-\.]+)*/?(?:\?[a-z0-9]+=[a-z0-9]+(?:&[a-z0-9]+=[a-z0-9]+)*)?(?:#[a-z0-9]+)?)', r'<a href="\1">\1</a>', text)
		return text

	@classmethod
	def spaces(cls, text):
		text = re.sub(r'[ ]+([\?!\.,:])[ ]+', r'\1 ', text)
		return text

	@classmethod
	def parse(cls, text):
		text = Markup.bold(text)
		text = Markup.italic(text)
		text = Markup.verbatim(text)
		text = Markup.hline(text)
		text = Markup.smileys(text)
		text = Markup.urls(text)
		text = Markup.paragraphs(text)
		text = Markup.spaces(text)
		return text