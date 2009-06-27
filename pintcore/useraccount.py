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

from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import db

from data.models import Account
from data.models import Token
from data.models import Message

class UserAccount:

    def __init__(self):
        self.account = Account()
        self.validAccount = False

    def getFromSession(self):
        
        user = users.get_current_user()
        if user:
            self.account = Account.gql("WHERE userId = :1", user.user_id()).get()
            if self.account:
                self.validAccount = True
            else:
                self.validAccount = False

    def getFromToken(self, token_code):
        
        token = Token.gql("WHERE code = :1", token_code).get()
        if token:
            if token.account and token.expires > datetime.now():
                self.account = token.account
                self.validAccount = True
            else:
                self.validAccount = False
        else:
            self.validAccount = False


    def getFromNickname(self, nickname):
        
        nickAccount = Account.gql( "WHERE nickname = :1", nickname ).get()
        if nickAccount:
            self.account = nickAccount
            self.validAccount = False
        else:
            self.validAccount = False


    def getKey(self):
        
        if self.validAcccount:
            return 

    def getNickname(self):
        
        if self.validAccount:
            return self.account.nickname
        else:
            return ''


    def getUserMessages(self, limit = 10):
        
        if self.validAccount:
            return Message.gql( "WHERE author = :1 ORDER BY date DESC", self.account.key() ).fetch( limit )
        else:
            return list()


    def getMessages(self, limit = 10):
 
        if self.validAccount:
            return Message.gql( "WHERE author IN :1 ORDER BY date DESC", self.account.following ).fetch( limit )
        else:
            return list()


    def getFollowers(self):
        
        if self.validAccount:
            return self.account.followers
        else:
            return list()


    def getFollowed(self):
        
        if self.validAccount:
            return self.account.followed
        else:
            return list()


    def isFollowing(self, user):
        
        if self.validAccount:
            return 