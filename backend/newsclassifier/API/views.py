from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from newsdataapi import NewsDataApiClient
# Create your views here.e
import os
import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext




api = NewsDataApiClient(apikey="pub_13758ca72c9d49ce4518063df9ac35af902ca")

from joblib import load

def get_articles():
    
    response = api.news_api(language="en", country="us")
    print(response)

# Given an array of with n strings, return an array with n probabilities it is positive
def probability_articles_is_positive(article_array):

    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, 'newsclassifier.joblib')   #full path to text.
    clf = load(file_path)
    classified = clf.predict_proba(article_array)
    probs = []
    for pair in classified:
        probs.append(pair[1])

    return probs

    

class GetArticles(APIView):
    """Get basic details of user"""

    def get(self, request):
        get_articles()
        reviews_news = ["In these times of economic uncertainty and the cost of living crisis, eating out is becoming more and more of a luxury for many people, rather than a regular pastime. Thankfully there are still plenty of places that offer great value for money, enabling people to enjoy dining out without breaking the bank. One such place is the Bells of St Mary's in Gronant. Situated just off the A548 coast road between Prestatyn and Ffynnongroyw, The Bells is popular all year round thanks to it's cut-price carvery meals, one user on Tripadvisor said: The Bells is a brilliant place with fantastic staff and offers amazing value for money.", "A shepherd has issued a desperate appeal for information after he found one of his lambs savaged to death on the Great Orme. National Trust tenant Dan Jones, who tends his flock on the limestone outcrop above Llandudno, shared a video on Twitter showing the damage a dog had caused to one of his sheep. The grim footage shows the sheep lying on the ground covered in blood at the top of a cliff, with two bite marks to its face and more bite marks on its leg. Dan appealed for anyone with information that could help track down the dog or its owner. He said: It is not a very nice day as I have a dead sheep here with me. As you can see, on her cheek there are two teeth marks where a dog as bitten her - killed her basically - along with marks on her back leg also."]
        print(probability_articles_is_positive(reviews_news))
        return Response({"message", "ok"}, status=status.HTTP_200_OK)

    