'''
Created on Apr 20, 2017

@author: NOADM
'''
import boto3
import gevent
import json
import random
from elasticsearch import Elasticsearch, exceptions, RequestsHttpConnection
import requests
from requests_aws4auth import AWS4Auth
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features


WORKERS = 10


QUEUE_NAME = "kwqueue"
WAIT_TIME = 10 # time to wait between each SQS poll
TOPIC_NAME = "tweettrend"
SNS_ARN = "arn:aws:sns:us-east-1:744025627651:tweettrend"
aws_access_key_id=""
aws_secret_access_key=""
REGION = "us-east-1"

awsauth = AWS4Auth(aws_access_key_id, aws_secret_access_key, REGION, 'es')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='kwqueue')
#sns = boto3.client('sns')

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username='',
    password=''
    )

es = Elasticsearch(
                   hosts=[{'host': 'search-kwdomain-c4a6knoxbx6xazhxtmc4qlx3vi.us-east-1.es.amazonaws.com', 'port': 443}],
                   use_ssl=True,
                   http_auth=awsauth,
                   verify_certs=True,
                   connection_class=RequestsHttpConnection
                   )

def task(pid):
    print ("[Task " + str(pid) + "] Starting ...")
    while True:
        for message in queue.receive_messages():
            tweet = json.loads(message.body)
            
            text = tweet["text"]
            print(text)
            
            response = natural_language_understanding.analyze(
                text=text,
                features=[features.Sentiment()])
            
            tweet["sentiment"] = response["sentiment"]["document"]["label"]
            
                # index tweet in ES
            res = es.index(index="tweets", doc_type="tweet", body=tweet)
                
                           
            print ("[Task " + str(pid) + ", tweetid " + " indexed")
            message.delete()
        gevent.sleep(WAIT_TIME)


if __name__ == "__main__":
    threads = [gevent.spawn(task, pid) for pid in range(1, WORKERS+1)]
    gevent.joinall(threads)
