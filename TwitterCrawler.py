import codecs
import json
from time import sleep
from bs4 import BeautifulSoup
from TwitterLogin import TwitterLogin
import threading
import sys
import requests
import os

username = ''
password = ''
searched_website_path = '../searched_websites/'
searched_results_path = '../search_results/billreilly/'

class TwitterCrawl:
    def __init__(self, browser_type):
        self.url = ''
        self.start_date = ''
        self.end_date = ''
        self.keyword = ''
        self.content = ''
        self.stop = False
        self.waittime = 1
        twitter_login = TwitterLogin(username, password, browser_type)
        self.browser = twitter_login.LoginWithSelenium()
        self.search_thread = None

    # @para: start_date and end_date has format: yyyy-mm-dd
    def advanced_search(self, start_date, end_date, keyword):
        self.start_date = start_date
        self.end_date = end_date
        self.keyword = keyword

        self.url = 'https://twitter.com/search?f=tweets&vertical=default&q=%22' + self.keyword + \
                   '%22%20since%3A' + self.start_date + '%20until%3A' + self.end_date + '&src=typd&lang=en'

        self.search_thread = threading.Thread(target=self.__do_advanced_search)
        self.search_thread.start()
        raw_input("Press Enter to stop...")
        self.stop = True
        try:
            self.content = self.browser.page_source.encode('utf-8').strip()
        except Exception:
            self.content = self.browser.page_source

        try:
            htmlfile = open(searched_website_path + keyword + '.html', 'w')
            htmlfile.write(self.content)
            htmlfile.close()
        except:
            #use unicode to save
            try:
                with codecs.open(searched_website_path + keyword + '.html', "w", encoding="utf-8") as f:
                    f.write(self.content)
            except:
                pass

        print 'The search has finished, parsing and saving data...'
        self.parse_and_save_data()

    def __do_advanced_search(self):
        #always scroll to bottom
        self.browser.get(self.url)
        count_repeat = 0
        prev_height = 0
        while not self.stop:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(self.waittime)
            current_height = self.browser.execute_script("return window.scrollY;")
            if prev_height < current_height:
                print 'crawling ' + str(current_height)
                prev_height = current_height
                count_repeat = 0
            else:
                count_repeat += 1
            if count_repeat > 3:
                print 'The search has exhaustive'
                break

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

def parse_and_save_data_indep(content, keyword):
    resultfile = open(searched_results_path + keyword + "_result.js", 'a')
    search_soup = BeautifulSoup(content, 'lxml')
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


def __parse_search_json(start_date, end_date, keyword, old_tweet_id, new_tweet_id, time):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'cookie': 'guest_id=v1%3A147699407786977931; eu_cn=1; moments_profile_moments_nav_tooltip_self=true; co=us; moments_user_moment_profile_create_moment_tooltip=true; moments_moment_guide_create_moment_tooltip=true; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0; geo_webclient=1; __utma=43838368.2131410032.1477169786.1477338634.1480450014.2; __utmz=43838368.1477338634.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); lang=en; _gat=1; kdt=mqUYule2B7ycQiEOx3NPe73nai2kJRWkXugplt8C; remember_checked_on=1; twid="u=98847310"; auth_token=043094244175949b290dc5ea13a242c7765d9f59; pid="v3:1480524214236319347010668"; _ga=GA1.2.2131410032.1477169786; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCM6p6LVYAToMY3NyZl9p%250AZCIlMzBlNDI3NDE1NTM3MGRjNWJkODViNGQyMjg5YzU5YTc6B2lkIiVhNjlm%250AMTMwNjhjNGY4MjY5MWRiM2VkOGZmNmMzZTI0YToJdXNlcmkETkrkBQ%253D%253D--a332306192c697e1a211e3a90be0555c724c8fdb'
    }
    os.system("mkdir " + searched_results_path +
              start_date + "-" + time.replace(' ', ''))
    resultfile = open(searched_results_path +
              start_date + "-" + time.replace(' ', '') + "/" + keyword + "_result.js", 'a')
    tweet_info = dict()
    found_time = False

    link = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&q='+keyword+'%20since%3A'+start_date+'%20until%3A'+end_date+'&src=typd&' \
           'include_available_features=1&include_entities=1&lang=en&max_position=TWEET-'+old_tweet_id+'-'+new_tweet_id+'-' \
           'BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
           'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
           '&reset_error_state=false'


    while True:
        try:
            content = requests.get(link, headers=headers).text.encode('utf-8')
            soup = BeautifulSoup(json.loads(content)['items_html'], 'lxml')
            all_tweet_blocks = soup.findAll('div', {
                'class': 'tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable original-tweet js-original-tweet '})
            for tweet_block in all_tweet_blocks:
                tweet_info['username'] = tweet_block['data-screen-name']
                tweet_info['timestamp'] = \
                    tweet_block.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})['title']
                tweet_info['content'] = tweet_block.find('p').text

                if time in tweet_info['timestamp']:
                   json.dump(tweet_info.copy(), resultfile)
                   resultfile.write('\n')
                   found_time = True

                if time not in tweet_info['timestamp'] and found_time and tweet_info['timestamp'] != '' and tweet_info['timestamp'] is not None:
                    print 'Finished crawling at %s' % tweet_info['timestamp']
                    resultfile.close()
                    sys.exit()

            old_tweet_id = all_tweet_blocks[len(all_tweet_blocks) - 1]['data-item-id']


            link = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + keyword + '%20since%3A' + start_date + '%20until%3A'+end_date+'&src=typd&' \
                    'include_available_features=1&include_entities=1&lang=en&max_position=TWEET-' + old_tweet_id + '-' + new_tweet_id + '-' \
                    'BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                    '&reset_error_state=false'


            print 'crawling keyword %s up to %s at time %s' % (keyword, old_tweet_id, tweet_info['timestamp'])
            tweet_info.clear()

        except Exception as e:
            print e
            sleep(2)

def advanced_search(start_date, end_date, keyword, time, init_old_id=None):

    headers = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'cookie':'guest_id=v1%3A147699407786977931; eu_cn=1; moments_profile_moments_nav_tooltip_self=true; co=us; moments_user_moment_profile_create_moment_tooltip=true; moments_moment_guide_create_moment_tooltip=true; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0; geo_webclient=1; __utma=43838368.2131410032.1477169786.1477338634.1480450014.2; __utmz=43838368.1477338634.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); lang=en; _gat=1; kdt=mqUYule2B7ycQiEOx3NPe73nai2kJRWkXugplt8C; remember_checked_on=1; twid="u=98847310"; auth_token=043094244175949b290dc5ea13a242c7765d9f59; pid="v3:1480524214236319347010668"; _ga=GA1.2.2131410032.1477169786; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCM6p6LVYAToMY3NyZl9p%250AZCIlMzBlNDI3NDE1NTM3MGRjNWJkODViNGQyMjg5YzU5YTc6B2lkIiVhNjlm%250AMTMwNjhjNGY4MjY5MWRiM2VkOGZmNmMzZTI0YToJdXNlcmkETkrkBQ%253D%253D--a332306192c697e1a211e3a90be0555c724c8fdb'
    }

    print 'crawling keyword %s' % keyword

    url = 'https://twitter.com/search?f=tweets&vertical=default&q='+keyword+'%20since%3A'+start_date+'%20until%3A'+ end_date +'&src=typd&lang=en'
    # content = urllib2.urlopen(url).read()
    content = requests.get(url, headers=headers).text.encode('utf-8')

    soup = BeautifulSoup(content, 'lxml')
    all_list = soup.findAll('li', {'class': 'js-stream-item'})
    new_id = all_list[0]['data-item-id']
    old_id = all_list[len(all_list) - 1]['data-item-id']
    if init_old_id is None:
        __parse_search_json(start_date, end_date, keyword, old_id, new_id, time)
    else:
        __parse_search_json(start_date, end_date, keyword, init_old_id, new_id, time)


if __name__ == '__main__':
    target_time = '6:21 AM'  ## time in browser + 3 hours
    start_date = '2017-01-31'
    end_date = '2017-02-01'

    # keywords= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    #            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #
    # for i in range(26):
    #     t = threading.Thread(target=advanced_search, args=(start_date, end_date, keywords[i], target_time, '826391076852359168'))
    #     t.start()

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    keyword = sys.argv[3]
    target_time = sys.argv[4]
    near_tweet_id = sys.argv[5]

    advanced_search(start_date, end_date, keyword, target_time, near_tweet_id)

