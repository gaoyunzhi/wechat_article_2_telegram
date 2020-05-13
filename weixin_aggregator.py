#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_util import log_on_fail
import sys
import os
from telegram.ext import Updater
import export_to_telegraph
import yaml
from soup_get import SoupGet
from db import DB
import threading

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)
export_to_telegraph.token = credential['telegraph_token']

tele = Updater(credential['bot_token'], use_context=True) # @contribute_bot
debug_group = tele.bot.get_chat(-1001198682178)
channel = tele.bot.get_chat(-1001402364957)

sg = SoupGet()
db = DB()

def processUser(user):
	url = sg.getAccountNewArticle(user)
	if not url:
		return
	wx_url = sg.getArticleUrl(url) # populate cache, because we need specific header
	if wx_url in db.existing.items:
		return
	r = export_to_telegraph.export(
		wx_url, force=True, force_cache=True)
	if not r:
		return
	message = '[%s](%s) | [原文](%s) \n#%s' % (r, r, wx_url, user)
	channel.send_message(message, parse_mode='Markdown')
	# todo: add more tags
	if 'test' not in sys.argv:
		db.existing.add(wx_url)

@log_on_fail(debug_group)
def loopImp():
	db.reload()
	for user in db.users.items:
		processUser(user)
	print('loop finished')
	command = 'git add . > /dev/null 2>&1 && git commit -m auto_commit > /dev/null 2>&1 && git push -u -f > /dev/null 2>&1'
	os.system(command)
	print('commit finished')

def loop():
	loopImp()
	threading.Timer(60 * 60, loop).start() 

if __name__ == '__main__':
	print('=====start======')
	if 'once' not in sys.argv:
		threading.Timer(1, loop).start()
	else:
		loopImp()