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

class AccountIO:

    def __init__(self):
        self.account = None

    def getFromSession(self):

        user = users.get_current_user()
        if user:
            self.account = Account.gql("WHERE userId = :1", user.user_id()).get()

    def getFromToken(self, token_code):

        token = Token.gql("WHERE code = :1", token_code).get()
        if token:
            if token.account and token.expires > datetime.now():
                self.account = token.account


    def getFromNickname(self, nickname):

        nickAccount = Account.gql( "WHERE nickname = :1", nickname ).get()
        if nickAccount:
            self.account = nickAccount

    def getFollowers(self, account = None):

        if account:
            return Account.gql("WHERE following = :1", account.key())
        elif self.account:
            return Account.gql("WHERE following = :1", self.account.key())
        else:
            return None

    def getFollowed(self, account = None):

        if account:
            return account.following
        elif self.account:
            return self.account.following
        else:
            return None

    def isFollowing(self, user, account = None):

        if account and user:
            if self.account.key() not in user.getFollowed():
                return False
            else:
                return True
        else:
            return None
