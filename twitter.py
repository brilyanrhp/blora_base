import tweepy
import constants
import time
import _json
from requests_oauthlib import OAuth1
import requests
import os
from async_upload import VideoTweet

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
                    d = dict(message = message, sender_id = sender_id, id = dm[x].id, media = None, shorted_media_url = None)
                    dms.append(d)
                    dms.reverse()

                else:
                    print("dm mengandung media")
                    media_type = dm[x].message_create['message_data']['attachment']['media']['type']
                    print(media_type)
                    if media_type == 'photo':
                        print("medianya foto")
                        attachment = dm[x].message_create['message_data']['attachment']
                        d = dict(message = message, sender_id = sender_id, id=dm[x].id,media = attachment['media']['media_url'], shorted_media_url = attachment['media']['url'], type = 'photo')
                        dms.append(d)
                        dms.reverse()
                    elif media_type == 'animated_gif':
                        print("medianya foto")
                        attachment = dm[x].message_create['message_data']['attachment']
                        d = dict(message = message, sender_id = sender_id, id=dm[x].id,media = attachment['media']['media_url'], shorted_media_url = attachment['media']['url'], type = 'animated_gif')
                        dms.append(d)
                        dms.reverse()
                    elif media_type == 'video':
                        print("medianya video")
                        attachment = dm[x].message_create['message_data']['attachment']
                        media = dm[x].message_create['message_data']['attachment']['media']
                        media_url = media['video_info']['variants'][0]
                        video_url = media_url['url']
                        print("video url "+str(video_url))
                        d = dict(message=message, sender_id=sender_id, id=dm[x].id, media=video_url, shorted_media_url=attachment['media']['url'], type='video')
                        dms.append(d)
                        dms.reverse()

            print(str(len(dms)) +" dikumpulkan")
            time.sleep(60)
            return dms
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def delete_dm(self, id):
        print("menghapus dm dengan id "+str(id))
        try:
            self.api.destroy_direct_message(id)
            time.sleep(40)
        except Exception as ex:
            print(ex)
            time.sleep(40)
            pass

    def post_tweet(self, tweet):
        try:
            print("menerbitkan tweet")
            self.api.update_status(tweet)
        except Exception as ex:
            print(ex)
            pass

    def post_tweet_with_media(self, tweet, media_url, shorted_media_url, type):
        try:
            print("shorted url = "+shorted_media_url)
            print("mendownload media")
            arr = str(media_url).split('/')
            print(arr[len(arr)-1])
            if type == 'video':
                arr = arr[len(arr)-1].split("?tag=1")
                arr = arr[0]
            elif type == 'photo':
                arr = arr[len(arr)-1]
            elif type == 'animated_gif':
                arr = arr[len(arr)-1]

            auth = OAuth1(client_key= constants.CONSUMER_KEY,
                          client_secret= constants.CONSUMER_SECRET,
                          resource_owner_secret= constants.ACCESS_SECRET,
                          resource_owner_key= constants.ACCESS_KEY)
            r = requests.get(media_url, auth = auth)
            with open(arr, 'wb') as f:
                f.write(r.content)

            print("media terdownload")
            if shorted_media_url in tweet:
                print("shorted url "+ str(shorted_media_url))
                tweet = tweet.replace(shorted_media_url, "")
            else:
                print("ga ada")

            if type == 'video':
                videoTweet = VideoTweet(arr)
                videoTweet.upload_init()
                videoTweet.upload_append()
                videoTweet.upload_finalize()
                videoTweet.tweet(tweet)
            elif type == 'photo':
                self.api.update_with_media(filename=arr, status=tweet)
            elif type == 'animated_gif':
                self.api.update_with_media(filename=arr, status=tweet)
            os.remove(arr)
            print("upload media sukses")
        except Exception as e:
            print(e)
            pass








