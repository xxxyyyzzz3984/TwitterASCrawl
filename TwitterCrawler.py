import urllib2
import urllib
from bs4 import BeautifulSoup
import re

image_folder_path = "../profileimages/"

def CrawlTwitProfileImage(twitter_page_link):
    page = urllib2.urlopen(twitter_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"data-user-id": True})
    for id_span in id_spans:

        for img_tag in id_span.findChildren("img", {"src": True}):
            if 'profile_image' in img_tag['src'] and 'default_' not in img_tag:
                img_link_str = img_tag['src']
                img_link_str = re.sub('_bigger', '',
                                      img_link_str)  # remove the "_bigger" substring, to achieve the bigger image

                print "crawling the image " + img_link_str

                user_id_str = id_span['href'].strip('/')
                f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
                f.write(urllib.urlopen(img_link_str).read())
                f.close()


CrawlTwitProfileImage('file:///home/xyh3984/Profile%20image%20project/image%20crawler/twitterwebsite/trump1.html')