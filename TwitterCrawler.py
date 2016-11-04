import argparse
import json
import threading
import time

from bs4 import BeautifulSoup
from TwitterLogin import TwitterLogin

username = ''
password = ''
searched_website_path = '../searched_websites/'
searched_results_path = '../search_results/'

class TwitterCrawl:
    def __init__(self):
        self.url = ''
        self.start_date = ''
        self.end_date = ''
        self.keyword = ''
        self.content = ''
        self.stop = False
        self.waittime = 1
        twitter_login = TwitterLogin(username, password)
        self.browser = twitter_login.LoginWithSelenium()
        self.search_thread = None

    # @para: start_date and end_date has format: yyyy-mm-dd
    def advanced_search(self, start_date, end_date, keyword):
        self.start_date = start_date
        self.end_date = end_date
        self.keyword = keyword

        self.url = 'https://twitter.com/search?q=' + self.keyword + '%20since%3A' + self.start_date + \
                   '%20until%3A'+ self.end_date + '&src=typd&lang=en'

        self.search_thread = threading.Thread(target=self.__do_advanced_search)
        self.search_thread.start()
        raw_input("Press Enter to stop...")
        self.stop = True
        self.content = self.browser.page_source.encode('utf-8').strip()
        htmlfile = open(searched_website_path + keyword+'.html', 'w')
        htmlfile.write(self.content)
        htmlfile.close()
        print 'The search has finished, parsing and saving data...'
        self.parse_and_save_data()

    def __do_advanced_search(self):
        #always scroll to bottom
        self.browser.get(self.url)
        while not self.stop:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.waittime)

    def parse_and_save_data(self):

        resultfile = open(searched_results_path + self.keyword + "_result.js", 'a')
        search_soup = BeautifulSoup(self.content, 'lxml')
        tweets_div_all = search_soup.findAll('div', {'data-tweet-id': True})

        for tweet_all in tweets_div_all:
            tweet_info = dict()
            username = tweet_all.find('span', {'class': 'username js-action-profile-name'}).find('b').text
            content = tweet_all.find('p').text.strip()
            timestamp = tweet_all.find('small').find('a')['title']
            tweet_info['username'] = username
            tweet_info['tweet_content'] = content
            tweet_info['create_time'] = timestamp
            json.dump(tweet_info.copy(), resultfile)
            resultfile.write('\n')

        resultfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='-s for start time, -e for endtime, -k for keyword')
    parser.add_argument('-s', '--start')
    parser.add_argument('-e', '--end')
    parser.add_argument('-k', '--keyword')
    args = parser.parse_args()

    twitter_crawl = TwitterCrawl()
    twitter_crawl.advanced_search(args.start, args.end, args.keyword)



