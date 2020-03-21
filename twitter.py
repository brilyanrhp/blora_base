import tweepy
import constants
import time
import _json
from requests_oauthlib import OAuth1
import requests
import os

class Twitter:
    def __init__(self):
        print("memproses twitter")
        self.inits = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        self.inits.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
        self.api = tweepy.API(self.inits)

    def read_dm(self):
        print("mendapatkan pesan dm")
        dms = list()
        try:
            api = self.api
            dm = api.list_direct_messages()
            for x in range (len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = str(dm[x].message_create['message_data'])
                json_data = _json.encode_basestring(message_data)
                print("mendapatkan pesan >>> " +str(message)+" dari id pengirim "+str(sender_id))
                if "attachment" not in json_data:
                    print("dm tidak mengandung media")
                    d = dict(message = message, sender_id = sender_id, id = dm[x].id, media = None)
                    dms.append(d)
                    dms.reverse()

                else:
                    print("dm mengandung media")
                    attachment = dm[x].message_create['message_data']['attachment']
                    d = dict(message=message, sender_id=sender_id, id=dm[x].id, media = attachment['media']['media_url'])
                    dms.append(d)
                    dms.reverse()



            print(str(len(dms)) +" dikumpulkan")
            time.sleep(30)
            return dms
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def delete_dm(self, id):
        print("menghapus dm dengan id "+str(id))
        try:
            self.api.destroy_direct_message(id)
            time.sleep(30)
        except Exception as ex:
            print(ex)
            time.sleep(40)
            pass

    def post_tweet(self, tweet):
        print("menerbitkan tweet")
        self.api.update_status(tweet)
        time.sleep(30)

    def post_tweet_with_media(self, tweet, media_url):
        print("mendownload media")
        arr = str(media_url).split("/")
        auth = OAuth1(client_key= constants.CONSUMER_KEY,
                      client_secret= constants.CONSUMER_SECRET,
                      resource_owner_secret= constants.ACCESS_SECRET,
                      resource_owner_key= constants.ACCESS_KEY)
        r = requests.get(media_url, auth = auth)
        with open(arr[9], 'wb') as f:
            f.write(r.content)
        print("media terdownload")
        tweet = tweet.replace("https://", "")
        self.api.update_with_media(filename=arr[9], status = tweet)
        os.remove(arr[9])
        print("media terupload")

    #pancing








