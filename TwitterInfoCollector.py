import tweepy
import time
import json

#figerprint can be id / screen name / user name
def get_user_profile(user_fingerprint, api):
    getuser = api.get_user(user_fingerprint)
    user_id = getuser.id
    screen_name = getuser.screen_name
    location = getuser.location
    time_zone = getuser.time_zone
    created_at = str(getuser.created_at)
    bio = getuser.description
    personal_website = getuser.url
    profile_pic_url = getuser.profile_image_url
    profile_background_image_url = getuser.profile_background_image_url

    user_profile = dict()
    user_profile.clear()

    user_profile['id'] = user_id
    user_profile['screen_name'] = screen_name

    if location is not None and location != '':
        user_profile['location'] = location

    if time_zone is not None and time_zone != '':
        user_profile['time_zone'] = time_zone

    if created_at is not None and created_at != '':
        user_profile['created_at'] = created_at

    if bio is not None or bio != '':
        user_profile['bio'] = bio

    if personal_website is not None and personal_website != '':
        user_profile['personal_website'] = personal_website

    if profile_pic_url is not None and profile_pic_url != '':
        user_profile['profile_pic_url'] = profile_pic_url

    if profile_background_image_url is not None and profile_background_image_url != '':
        user_profile['profile_background_pic_url'] = profile_background_image_url

    return user_profile.copy()

if __name__ == '__main__':
    consumer_key = 'eZJNcIYx1HpY5jivQ6i2SKXq6'
    consumer_secret = 'iGMNhcYuYxQfas1ye0P3V2O2D2dzGp24TiXhvd4dY0T48Jh3uQ'
    access_token = '790648054152036352-4dfsTFDeRyaVkJeodTKomRcIx1uFl6H'
    access_token_secret = '46UkOEr3ECcyD1GFPPl8s5IxjwLvkBWkvUL91K2axJ8Wp'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    first_time_result_usernames_path = '../search_results/Twitter_Firsttime_NameList.txt'
    output_file_path = '../search_results/Twitter_Firsttime_User_Profile.txt'

    with open(first_time_result_usernames_path) as f:
        for name in f:
            output_file = open(output_file_path, 'a')
            while True:
                try:
                    user_profile_json = get_user_profile(name, api= api)
                    json.dump(user_profile_json, output_file)
                    output_file.write('\n')
                    output_file.close()
                    break
                except tweepy.RateLimitError:
                    print 'Limit exceeds, sleeping for 15 minutes...'
                    time.sleep(15 * 60)

                except tweepy.TweepError as e:
                    print 'Cannot find user ' + name +'. Skipping...'
                    break

