#!/usr/bin/env python
import curlconverter
import requests
import time
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# NOTE: Base url to get absolute URLs from href
base_url = "https://magic.wizards.com"
news_archive_url = 'https://magic.wizards.com/en/news/archive'

# Browser cookies and headers to reuse and avoid server to know we are not a web browser ;)
# To get this format from a curl request copied from a browser just use: curlconverter.com
cookies = {
    '_swb': '51ea1fec-00a8-4d36-932a-7c4f9c53e223',
}

headers = {
    'authority': 'magic.wizards.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': '_swb=51ea1fec-00a8-4d36-932a-7c4f9c53e223',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://magic.wizards.com/en',
    'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


# Compile articles of the 5 most recent pages
articles_data = []
for i in range(1, 6):
    print(f"Downloading contents of page {i}... ", end='')
    # First page does not use "page"
    if i==1:
        url = news_archive_url
    else:
        url = f"{news_archive_url}?page={i}"
    response = requests.get(news_archive_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_data += soup.select("article")
    print("Done! Waiting 3 seconds to download the next")
    time.sleep(3)

# Create Feed
fg = FeedGenerator()
fg.title('Magic: The Gathering News')
fg.link(href=news_archive_url)
fg.logo('https://magic.wizards.com/assets/favicon.ico')
fg.description('Unofficial RSS feed for Magic news')
fg.language('en')

for article in articles_data:
    # Entry data
    title = article.select_one("a[data-link-type]").text
    link = base_url + article.select_one("a[data-link-type]").get("href")
    description = article.select_one(".css-p4BJO").text

    # Entry
    fe = fg.add_entry()
    fe.id(link)
    fe.title(title)
    fe.link(href=link)
    fe.description(description)
    
# Generate the feed file
fg.rss_file('magic_news_rss.xml')

