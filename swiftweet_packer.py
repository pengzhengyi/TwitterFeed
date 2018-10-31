from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import deque
import json
import os
import platform
import random
import signal
import sys
import threading
import time

twitter_url = 'https://twitter.com/'
request_url = 'https://twitter.com/search?q=Taylor%20Swift'
cwd = os.getcwd()

tweets = deque(maxlen=1000)
tweets_ids = set()

def determine_os():
    os = platform.system().lower()
    if os == 'linux':
        return 'linux'
    elif os == 'darwin':
        return 'mac'
    else:
        sys.exit('unsupported os type %s' % os)

chromedriver_path = "%s/chromedriver_%s" % (cwd, determine_os())

def make_soup(quiet=True):
    # driver = webdriver.Safari()
    options = Options()
    options.headless = quiet
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.implicitly_wait(30)
    driver.get(request_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def cook_soup(soup):
    return [parse_tweet(tweet_html) for tweet_html in soup.find_all('div', class_='tweet')]

def user_url(user_screen_name):
    return twitter_url + user_screen_name

def parse_tweet(tweet_html):
    """
    each tweet is in class tweet
    properties:
        created_at: a.tweet_timestamp title; span._timestamp data-time
        id: div.tweet data-item-id
        id_str: str(id)
        text: p.tweet-text 
        user: a.account-group
        entities
    """
    tweet = {}
    user = {}
    created_at_hr = tweet_html.select('a.tweet-timestamp')[0]['title'] # human readable
    created_at_htc = tweet_html.select('span._timestamp')[0]['data-time']
    id_str = tweet_html['data-item-id']
    id = int(id_str)
    text_section = tweet_html.select('p.tweet-text')[0]
    text = text_section.text
    text_with_html_tags = ''.join(str(tag) for tag in text_section.contents)
    
    user_id_str = tweet_html['data-user-id']
    user_id = int(user_id_str)
    user_name = tweet_html['data-name']
    user_screen_name = tweet_html['data-screen-name']
    user_profile_image_url_https = tweet_html.select('img.avatar')[0]['src']

    tweet['created_at'] = created_at_hr
    tweet['id'] = id
    tweet['id_str'] = id_str
    tweet['text'] = text
    tweet['tagged_text'] = text_with_html_tags
    tweet['user'] = user

    user['id'] = user_id
    user['id_str'] = user_id_str
    user['name'] = user_name
    user['screen_name'] = user_screen_name
    user['profile_image_url_https'] = user_profile_image_url_https
    user['url'] = user_url(user_screen_name)
    return tweet

def pull_tweets():
    count = 0
    for tweet in cook_soup(make_soup()):
        tid = tweet['id']
        if tid not in tweets_ids:
            tweets_ids.add(tid)
            tweets.append(tweet)
            count += 1
    print("%s new tweets has been pulled" % count)

t = None
def autoload():
    global t
    pull_tweets()
    t = threading.Timer(10, autoload)
    t.daemon = True
    t.start()
    

def pack_tweets(most_recent=50): # cooked soup
    return json.dumps(random.sample(tweets, min(most_recent, len(tweets))))

def refridge(fridge):
    with open(fridge, 'w') as fdg:
        json.dump(list(tweets), fdg)

def defrost(fridge):
    if os.stat(fridge).st_size:
        with open(fridge, 'r') as fgd:
            tweets.extendleft(json.load(fgd))

def packing(fridge='swiftweets.json'):
    def stage(signum, f):
        t.cancel()
        refridge(fridge)
        print("soup has been put inside the fridge")
        signal.signal(signal.SIGINT, orig_sigint_handler)
    orig_sigint_handler = signal.signal(signal.SIGINT, stage)
    print("Type CTRL-C to stop packing")
    defrost(fridge)
    autoload()

packing()
