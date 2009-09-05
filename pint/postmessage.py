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

from pintcore.accountio import AccountIO
from pintcore.postio import PostWrite

from data.models import Account
from data.models import TextMsg, QuoteMsg, LinkMsg, ImageMsg, EmbedMsg
from data.models import Image

# Do you think we could put all the actions in another file?
class PostMessage(webapp.RequestHandler):
    def post(self,type):

        if type != '':
            user = AccountIO()
            user.getFromSession()

            if user.account:
                postwrite = PostWrite(user.account)

                if type == 'text':
                    postwrite.postText(self.request.get('title'), self.request.get('textpost'))
                elif type == 'quote':
                    postwrite.postQuote(self.request.get('quote'), self.request.get('source'))
                elif type == 'link':
                    postwrite.postLink(self.request.get('title'), self.request.get('url'), self.request.get('description'))
                elif type == 'image':
                    if self.request.get('imageurl') != '':
                        postwrite.postImage(self.request.get('imageurl'), self.request.get('caption'))
                    # Todo: add image upload code.
                elif type == 'embed':
                    postwrite.postEmbed(self.request.get('embedcode'), self.request.get('description'))


        if self.request.headers['referer'].startswith('http://pinstme.appspot.com/share'):
            path = os.path.join(os.path.dirname(__file__), '../views/bookmarklet-exit.html')
            self.response.out.write(template.render(path,{'message':'Message Posted!'}))
        else:
            self.redirect('/')

    def get(self):

        user = AccountIO()
        user.getFromSession()

        # Template values, yay!
        if user.account:
            template_values = {
                'nickname': user.account.nickname
            }
        else:
            self.redirect('/')

        # We get the template path then show it
        path = os.path.join(os.path.dirname(__file__), '../views/post.html')
        self.response.out.write(template.render(path, template_values))
