import cached_url
from bs4 import BeautifulSoup
import yaml

domain = 'https://weixin.sogou.com'
account_search_prefix = '/weixin?type=1&query='

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

class SoupGet(object):
	def getAccountNewArticle(self, name):
		content = cached_url.get(
			domain + account_search_prefix + name)
		soup = BeautifulSoup(content, 'html.parser')
		item = soup.find('a', uigs='account_article_0')
		return item and domain + item['href']

	def getArticle(self, url):
		return cached_url.get(
			url,
			force_cache=True,
			headers = {'cookie': credential['cookie']})