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
from tags import getTags
import readee
from bs4 import BeautifulSoup
import time
import cached_url
from telegram_util import AlbumResult as Result
import album_sender
import random

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)
export_to_telegraph.token = credential['telegraph_token']

tele = Updater(credential['bot_token'], use_context=True) # @contribute_bot
debug_group = tele.bot.get_chat(-1001198682178)
channel = tele.bot.get_chat(-1001402364957)

sg = SoupGet()
db = DB()

def sendTelegraph(r, user, source_url):
	tags = ' '.join(['#%s' % x for x in getTags(r)])
	message = '[%s](%s)\n#%s %s' % (r, r, user, tags)
	if source_url:
		message += ' [source](%s)' % source_url
	try:
		return channel.send_message(message, parse_mode='Markdown')
	except Exception as e:
		print(str(e))
		print(message, source_url)

def getSoup(telegraph_url):
	content = cached_url.get('https://' + telegraph_url, force_cache=True)
	return BeautifulSoup(content, 'html.parser')

def getTitle(telegraph_url):
	return getSoup(telegraph_url).find('h1').text.strip()

def sendImage(user, telegraph_url, source_url):
	r = Result()
	r.cap = getTitle(telegraph_url) + ' #%s' % user
	r.imgs = [x['src'] for x in getSoup(telegraph_url).find_all('img')]
	if not r.imgs:
		return
	return album_sender.send(channel, source_url, r)

def goodUrl(url):
	return url.count('*') <= 1 and url.count('..') == 0

def getGoodUrl(*args):
	for url in args:
		if goodUrl(url):
			return url

def processUser(user):
	if 'test' not in str(sys.argv):
		time.sleep(60)

	url = sg.getAccountNewArticle(user)
	if not url:
		print('no first article:', user)
		return
	wx_url = sg.getArticleUrl(url) # populate cache, because we need specific header
	print(wx_url)

	telegraph_url = export_to_telegraph.export(wx_url, force_cache=True)
	telegraph_force_url = export_to_telegraph.export(wx_url, force_cache=True, force=True)
	if not telegraph_force_url:
		return

	title = getTitle(telegraph_force_url)
	if title in db.existing.items:
		return

	source_url = getGoodUrl(url, wx_url, telegraph_force_url)
	user = user.replace(' ', '\_')
	if telegraph_url:
		sent = sendTelegraph(telegraph_url, user, source_url)
	else:
		sent = sendImage(user, telegraph_force_url, source_url)

	if 'test' not in str(sys.argv):
		db.existing.add(title)
	return sent

@log_on_fail(debug_group)
def loopImp():
	db.reload()
	users = list(db.users.items)
	random.shuffle(users)
	for user in users:
		if processUser(user):
			break
	print('loop finished')
	command = 'git add . > /dev/null 2>&1 && git commit -m auto_commit > /dev/null 2>&1 && git push -u -f > /dev/null 2>&1'
	os.system(command)
	print('commit finished')

def loop():
	loopImp()
	threading.Timer(30 * 60, loop).start() 

if __name__ == '__main__':
	print('=====start======')
	if 'once' not in sys.argv:
		threading.Timer(1, loop).start()
	else:
		loopImp()