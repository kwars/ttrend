from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse
# from .forms import MyForm
import requests
import json
import ast
import urllib.request
from django.views.decorators.csrf import csrf_exempt
import socket



def Index(Request):
    return render(Request, 'googleMap/map.html')



def Post(Request):
    if Request.method == "POST":
        msg = Request.POST.get('Search', None)

        host = 'https://search-kwdomain-c4a6knoxbx6xazhxtmc4qlx3vi.us-east-1.es.amazonaws.com/tweets/_search?q='

        url = host + msg
        response = requests.get(url)
        r = json.loads(response.text)
        tweet = [res['_source']['text'] for res in r['hits']['hits']]
        data = [res['_source']['coordinates'] for res in r['hits']['hits']]
        sentiment = [res['_source']['sentiment'] for res in r['hits']['hits']]
        #print (data[0][0])
        hits = len(data)
        length = {'hits': hits}
        coordinates = {}
        tweets = {}
        for i in range(hits):
            #if (data[i][0] < - 90):
             #   data[i][0] = data[i][0] + 180
            coordinates[i] = {'lat': data[i][1], 'lng': data[i][0]}
            tweets[i] = {'tweet': tweet[i],
                         'sentiment': sentiment[i]
                         }
            
            
            print(tweets[i])
            print(coordinates[i])

        data = {'coordinates': coordinates, 'length': length,'tweets': tweets}

        return JsonResponse(data)       