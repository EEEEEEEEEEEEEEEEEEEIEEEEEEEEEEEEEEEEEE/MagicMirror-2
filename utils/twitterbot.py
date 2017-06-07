import requests
import math, random
import config
from lxml import etree

url = "https://twitter.com/"
proxies = None

def getTweet(who=None, proxies=proxies):
    who = who if who else "tinycarebot"
    return _scrapeTweet(who, proxies)


def _scrapeTweet(who, proxies):
    try:
    	reqUrl = url + who
        resp = requests.get(reqUrl, proxies=proxies) if proxies else requests.get(reqUrl)
        page = etree.HTML(resp.content)
        lst = page.cssselect(".js-tweet-text.tweet-text")
        tweets = [item.xpath("text()")[0] for item in lst]
        tweetNo = int(math.floor(random.random()*len(tweets)))
        #print tweetNo, len(tweets)
        return {"author": who, "content": tweets[tweetNo]}
    except Exception as e:
        print e
        return {"error": "Can't scrape tweets. Maybe the user is private or doesn\'t exist?"}
