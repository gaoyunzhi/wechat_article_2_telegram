#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import yaml
with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @contribute_bot
debug_group = tele.bot.get_chat(-1001198682178)
channel = tele.bot.get_chat(-1001402364957)

message = '''
#Rainbow\\_Academy
'''
debug_group.send_message(message, parse_mode='Markdown')
