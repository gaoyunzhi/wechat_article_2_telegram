import cached_url
from bs4 import BeautifulSoup

account_search_prefix = 'https://weixin.sogou.com/weixin?type=1&query='

class SoupGet(object):
	def getAccountNewArticle(self, name):
		soup = BeautifulSoup(cached_url.get(
			account_search_prefix + name), 'html.parser')
		item = soup.find('a', uigs='account_article_0')
		return item and item['href']