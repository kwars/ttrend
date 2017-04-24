import boto3
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
#Enter your twitterAPI keys here 
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

sqs = boto3.client('sqs')

class StdOutListener(StreamListener):

    def on_data(self, data):
        data_json = json.loads(data)
        try:
            coordinates = data_json['place']['bounding_box']['coordinates']
            tweet = data_json['text']
            place = data_json['place']

            if place is not None:
                if coordinates[0] is not None and len(coordinates[0]) > 0:
                    avg_x = 0
                    avg_y = 0
                    for c in coordinates[0]:
                        avg_x = (avg_x + c[0])
                        avg_y = (avg_y + c[1])
                    avg_x /= len(coordinates[0])
                    avg_y /= len(coordinates[0])
                    coordinates = [avg_x, avg_y]
                print (coordinates)
                e_data = {
                    "text": tweet,
                    "coordinates": coordinates

                }
                response = sqs.send_message(QueueUrl = 'https://sqs.us-east-1.amazonaws.com/744025627651/kwqueue',MessageBody = json.dumps(e_data))
                print (response)
        except (KeyError, TypeError):
            pass
        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, StdOutListener())
    stream.filter(track=['love','travel','Trump','pizza','money','NBA','haha','emotion','cloud computing','whatever','this course sucks'])


