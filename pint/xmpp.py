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

from google.appengine.api import xmpp
from google.appengine.ext import webapp

class XMPPHandler(webapp.RequestHandler):
  def post(self):
    message = xmpp.Message(self.request.POST)

    if message.to.startswith('construct@pintme.appspotchat.com'):
        if message.to.endswith('/bot'):
            if message.body.lower() == 'help':
                message.reply("Commands are 'help', 'status'")
            else:
                message.reply("Type 'help' for commands.")
        else:
            message.reply('Welcome to construct.')
