import cached_url
from bs4 import BeautifulSoup

domain = 'https://weixin.sogou.com'
account_search_prefix = '/weixin?type=1&query='

class SoupGet(object):
	def getAccountNewArticle(self, name):
		soup = BeautifulSoup(cached_url.get(
			domain + account_search_prefix + name), 'html.parser')
		item = soup.find('a', uigs='account_article_0')
		return item and domain + item['href']