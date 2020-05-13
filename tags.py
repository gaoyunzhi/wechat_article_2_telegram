from textrank4zh import TextRank4Keyword
from bs4 import BeautifulSoup
import cached_url

def getTags(url):
	tr4w = TextRank4Keyword()
	content = cached_url.get('https://' + url, force_cache=True)
	b = BeautifulSoup(content, 'html.parser')
	tr4w.analyze(text=b.text, lower=True, window=2)
	candidate = [x.word for x in tr4w.get_keywords(20, word_min_len=1)]
	candidate = [x for x in candidate if len(x) >= 2]
	return candidate[:5]