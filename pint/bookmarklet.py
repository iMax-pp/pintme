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
import urllib
import urlparse

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from pintcore.useraccount import UserAccount
from libs.BeautifulSoup import BeautifulSoup

from data.models import Account
from data.models import Message

class Bookmarklet(webapp.RequestHandler):
    def get(self):

        shareURL = urllib.unquote(self.request.get('u'))
        shareSelection = urllib.unquote(self.request.get('s'))

        shareURLParts = urlparse.urlparse(shareURL)
        if shareURLParts[2] != '':
            shareURLDir = re.search('(/.*)',shareURLParts[2]).group(0)
        else:
            shareURLDir = ''
        page = urlfetch.fetch(shareURL)
        pageSoup = BeautifulSoup(page.content)

        try:
            shareTitle =  pageSoup.html.head.title.string
        except AttributeError:
            shareTitle = urllib.unquote(self.request.get('t'))

        pageImgs = pageSoup.findAll('img')

        for image in pageImgs:
            #if not image['src'].startswith('http://'):
                #image['src'] = '/' + image['src']
            if image['src'].startswith('/'):
                image['src'] = shareURLParts[0] + '://' + shareURLParts[1] + shareURLDir + image['src']
            if 'alt' not in image:
                image['alt'] = 'Unnamed'

        template_values = {
            'url': shareURL,
            'title': shareTitle,
            'selection': shareSelection,
            'images': pageImgs
        }

        # We get the template path then show it
        path = os.path.join(os.path.dirname(__file__), '../views/bookmarklet.html')
        self.response.out.write(template.render(path, template_values))
