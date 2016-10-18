import urllib2
import urllib
from bs4 import BeautifulSoup
import re
import os.path

image_folder_path = "../profileimages/"
twitter_website_folder_path = "../twitterwebsite/todo/"

def CrawlTwitProfileImage(twitter_page_link):
    page = urllib2.urlopen(twitter_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"data-user-id": True})
    for id_span in id_spans:

        for img_tag in id_span.findChildren("img", {"src": True}):
            if 'profile_image' in img_tag['src'] and 'default_' not in img_tag:
                img_link_str = img_tag['src']
                img_link_str = re.sub('_bigger', '', img_link_str)  # remove the "_bigger" substring, to achieve the bigger image

                print "crawling the image " + img_link_str

                user_id_str = id_span['href'].strip('/')
                f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
                f.write(urllib.urlopen(img_link_str).read())
                f.close()


for root, dirs, htmlfiles in os.walk(twitter_website_folder_path):
    for htmlfile in htmlfiles:
        abs_path_str = os.path.realpath(os.path.join(root, htmlfile))
        abs_path_url_str = "file://" + abs_path_str
        abs_path_url_str = re.sub(' ', '%20', abs_path_url_str) # replace all the spaces with %20
        CrawlTwitProfileImage(abs_path_url_str)