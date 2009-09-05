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

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

from data.models import Message, TextMsg, QuoteMsg, LinkMsg, ImageMsg, EmbedMsg
from data.models import Account

class PostRead:

    def getSentMessages(self, account, limit = 10):

        if account:
            return Message.gql( "WHERE author = :1 ORDER BY date DESC", account.key() ).fetch( limit )
        else:
            return list()

    def getMessages(self, account, limit = 10):

        if account:
            return Message.gql( "WHERE author IN :1 ORDER BY date DESC", account.following ).fetch( limit )
        else:
            return list()

    def getAllMessages(self, limit = 10):

        return Message.gql("ORDER BY date DESC").fetch(limit)


class PostWrite:

    def __init__(self,account):
        self.account = account;

    def postText(self,title,text):
        if text != '':
            message = TextMsg()
            message.author = self.account.key()
            message.title  = title
            message.text   = text
            message.put()

    def postQuote(self,quote,source):
        if quote != '':
            message = QuoteMsg()
            message.author = self.account.key()
            message.quote = quote
            message.source = source
            message.put()

    def postLink(self,title,url,description):
        if url != '':
            message = LinkMsg()
            message.author = self.account.key()
            message.title = title
            message.url = url
            message.description = description
            message.put()

    def postImage(self,imageurl,caption):
        if imageurl != '':
            message = ImageMsg()
            message.author = self.account.key()
            message.imageurl = imageurl
            message.caption = caption
            message.put()

    def postEmbed(self,embedcode,description):
        if embedcode != '':
            message = EmbedMsg()
            message.author = self.account.key()
            message.embedcode = embedcode
            message.description = description
            message.put()
