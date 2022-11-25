from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from newsdataapi import NewsDataApiClient
from django.http import JsonResponse
# Create your views here.e
import os
import re
import json

N_ARTICLES_WANTED = 100

api = NewsDataApiClient(apikey="pub_13758ca72c9d49ce4518063df9ac35af902ca")

from joblib import load

def get_articles():
    page = 1

    articles = []
    while(len(articles) < N_ARTICLES_WANTED):

        response = api.news_api(language="en", country="us", category='world,science', page=page)
        for article in response['results']:
            obj = {
                "title": article['title'],
                "image": article['image_url'],
                "video": article['video_url'],
                'description': article['description'],
                "content": article['content'],
                "link": article['link']
            }
            if obj['title'] != None and (obj['content'] != None or obj['description'] != None):
                articles.append(obj)

        page += 1



    return articles

# Given an array of with n strings, return an array with n probabilities it is positive
def add_probability_of_articles(article_data):
    
    titles = []
    descriptions = []
    for item in article_data:
        desc = ""
        if item['content'] == None:
            if item['description'] == None:
                # ajowdawd
                pass
            else:
                desc = item['description']
        else:
            desc = item['content']


        titles.append(item['title'])
        descriptions.append(desc)

    
    module_dir = os.path.dirname(__file__)  
    file_path_headline = os.path.join(module_dir, 'newsclassifier_headlines.joblib')   #full path to text.
    file_path_movie = os.path.join(module_dir, 'newsclassifier.joblib')  
    file_path_financial = os.path.join(module_dir, 'newsclassifier_financial.joblib')  
    clf_headLine = load(file_path_headline)
    clf_movie = load(file_path_movie)
    clf_financial = load(file_path_financial)
    classified_headline = clf_headLine.predict_proba(titles)
    classified_descriptions = clf_financial.predict_proba(descriptions)
    for i in range(len(article_data)):
        pair_headline = classified_headline[i]
        pair_descriptions= classified_descriptions[i]
        article_data[i]['probability_title'] = {
            "pos": pair_headline[0],
            "neg": pair_headline[1]
        }
        article_data[i]['probability_description'] = {
            "pos": pair_descriptions[0],
            "neg": pair_descriptions[1]
        }

 

    

class GetArticles(APIView):
    """Get basic details of user"""

    def get(self, request):
        articles = get_articles()
        
        add_probability_of_articles(articles)
        return JsonResponse(articles, status=status.HTTP_200_OK, safe=False)

    