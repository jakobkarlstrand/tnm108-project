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

import nltk
nltk.download('omw-1.4')
nltk.download('sentiwordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

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
    file_path_kaggle = os.path.join(module_dir, 'kaggle.joblib')  
    #clf_headLine = load(file_path_headline)
    #clf_movie = load(file_path_movie)
    clf_kaggle = load(file_path_kaggle)
   #classified_headline = clf_headLine.predict_proba(titles)
    classified_descriptions = clf_kaggle.predict_proba(descriptions)
    for i in range(len(article_data)):
        pair_descriptions= classified_descriptions[i]
        article_data[i]['probability_description'] = {
            "pos": pair_descriptions[0],
            "neg": pair_descriptions[1]
        }

 


def getSentimentWithWordNet(sentence):
 
    list(swn.senti_synsets('slow'))
    from nltk.tag import pos_tag
    token = nltk.word_tokenize(sentence)
    after_tagging = nltk.pos_tag(token)

    def penn_to_wn(tag):
        """
        Convert between the PennTreebank tags to simple Wordnet tags
        """
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None
    sentiment = 0.0
    tokens_count = 0
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    for word, tag in after_tagging:
                wn_tag = penn_to_wn(tag)
                if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                    continue
    
                lemma = lemmatizer.lemmatize(word, pos=wn_tag)
                if not lemma:
                    continue
    
                synsets = wn.synsets(lemma, pos=wn_tag)
                if not synsets:
                    continue
    
                # Take the first sense, the most common
                synset = synsets[0]
                swn_synset = swn.senti_synset(synset.name())
        
    
                sentiment += swn_synset.pos_score() - swn_synset.neg_score()
                tokens_count += 1
    return sentiment


    

class GetArticles(APIView):
    """Get basic details of user"""

    def get(self, request):
        #articles = get_articles()

        fake_articles = [{
            "title": "World First: Child Treated in the Womb For Rare Genetic Disorder",
            "content": "A child with the life-threatening condition Pompe disease was given treatment in the womb. Now, thanks to the treatment, Ayla Bashir was born without any complications associated with the disease. Pompe disease is a rare genetic disorder. There are different variants to the disease, with those that develop the condition in the womb having infantile-onset Pompe disease. The disease causes glycogen- the stored form of glucose- to build up in the body’s cells. Glycogen requires an enzyme called acid alfa glucosidase (GAA) to help break it down. People with Pompe disease are born with a deficiency in this enzyme, because of a mutation on the GAA gene. Ayla Bashir was born 16 months ago, and is like any other healthy child her age, meeting all of her milestones. Whilst she will need ongoing treatment for the rest of her life, Ayla is without any of the debilitating symptoms of Pompe. “She’s just a regular little 1½-year-old who keeps us on our toes,” Zahid Bashir, her father, told The Associated Press. Ayla’s parents, Zahid, and mother, Sobia, both carry a recessive gene that gives any child they conceive a 25% risk of developing Pompe. They had already lost two children in infancy to the disorder, when Sobia found out that Ayla also had the condition during a prenatal screening. Thankfully, at CSF Benioff Children’s Hospitals Dr Tippi MacKenzie, a fetal and paediatric surgeon, was launching a clinical trial to treat Pompe disease before birth, and looking for participants. Sobia was referred to the hospital in 2020, however, due to the pandemic was looked after by two institutions in Canada — The Ottawa Hospital and the Children’s Hospital of Eastern Ontario (CHEO). She began treatment in her 24th week of pregnancy. This involved biweekly infusions of the GAA enzyme directly into the umbilical cord. Ayla was born completely healthy, without any of the typical signs and symptoms of Pompe disease, such as muscle weakness and thickened heart muscles. Treatment for infantile-onset Pompe disease is relatively new, and only became available in 2006. Before that, babies born with the disorder were not expected to live past their first birthdays. However, even with this treatment, life expectancy for someone with infantile-onset Pompe disease is only 30 years. This is due to the mutation of the GAA gene affecting babies with the disease as they are developing in the womb. By the time the baby with Pompe disease is born, they have already suffered damage, due to the disease, causing problems with muscle tone and growth, and failure to gain weight. This affects all muscles in the body, including vital organs such as the heart. This new treatment could potentially mean a normal lifespan for those with Pompe’s disease. Dr. Ans van der Ploeg, who is the chair of the Center for Lysosomal and Metabolic Diseases at the Erasmus MC University in Rotterdam concluded that this was a promising result. “Further follow-up of this patient will be important,' but so far, the course of her development has been 'encouraging,' he wrote.",

        },
        {
            "title": "Congressman Donald McEachin dies at 61",
            "content": "Virginia Congressman Donald McEachin died on Monday at age 61, weeks after winning a fourth term representing all of Richmond, parts of Henrico and Chesterfield counties, and the Tri-Cities area in the 4th Congressional District. McEachin's death was sudden, but his illness was not. He had been suffering from the after-effects from the successful treatment of colorectal cancer eight years ago. “We are all devastated at the passing of our boss and friend, Congressman Donald McEachin, Tara Rountree, the Democratic congressman's chief of staff, said in a statement on Monday night. Valiantly, for years now, we have watched him fight and triumph over the secondary effects of his colorectal cancer from 2013, Rountree said. Tonight, he lost that battle and the people of Virginia’s Fourth Congressional district lost a hero who always, always fought for them and put them first."
        }]

        # for obj in articles:
        #     desc = ""
        #     if obj['content'] == None:
        #         if obj['description'] == None:
        #         # ajowdawd
        #             pass
        #         else:
        #             desc = obj['description']
        #     else:
        #         desc = obj['content']

        #     sentiment = getSentimentWithWordNet(desc)
        #     obj['sentiment'] = sentiment



        add_probability_of_articles(fake_articles)
        return JsonResponse(fake_articles, status=status.HTTP_200_OK, safe=False)

    