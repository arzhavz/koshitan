import re
import requests
from bs4 import BeautifulSoup as soup

def check_body_class(html):
	body_tag = html.find('body')
	if body_tag and 'search-results' in body_tag.get('class', []):
		return True
	else:
		return False

def Wallpapers(query):
	data = requests.get(f"https://wallpapers.com/search/{query}")
	html = soup(data.text, "html.parser")
	if check_body_class(html):
		results = []
		kw_contents = html.find("ul", {"class": "kw-contents"})
		contents = kw_contents.find_all("li")
		for content in contents:
			try:
				item = {
					"id": content.get("id", "N/A"),
					"title": content.find("figure").get("data-title", "N/A"),
					"desc": re.sub(r"</?p>", "", content.find("figure").get("data-desc", "N/A")),
					"alt": content.find("img").get("alt", "N/A"),
					"page": content.find("a").get("href", "N/A"),
					"url": f"https://wallpapers.com{content.find('img').get('data-src')}"
				}
			except Exception as e:
				pass
			results.append(item)
		return results if len(results) != 0 else False
	else:
		return False