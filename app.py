from flask import Flask, request
from get_data import *
from util import *
import json
from flask_cors import CORS
import pandas as pd
from distutils.util import strtobool
from KNN import KNN
from Bayes import Bayes
from KeyWords import KeyWords


app = Flask(__name__)
CORS(app)

clean_labeled_tweets = pd.read_csv("data/clean_labeled_tweets.csv")

fp  = open('corpus/negative.txt')
negative_dict= [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]

fp  = open('corpus/positive.txt')
positive_dict= [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]



@app.route("/search/<query>/<count>")
def search(query,count):

    new_tweets = search_tweets(query,int(count))
    return json.dumps(df_to_object(new_tweets))


@app.route("/classifier/KNN/<k>/<distance>/<c>")
def knn_classifier(k,distance,c):

    k = int(k)
    if distance == "naiveDistance":
        knn_classifier = KNN(k,naive_distance)
    elif distance == "levenshtein":
        knn_classifier = KNN(k,levenshtein_distance)
    else : 
        knn_classifier = KNN(k,naive_distance)

    return json.dumps(classifierResults_to_object(knn_classifier,int(c),clean_labeled_tweets))



@app.route("/classifier/keyWords/<c>")
def keyWords_classifier(c):

    key_words_classifier = KeyWords(positive_dict,negative_dict)
    
    return json.dumps(classifierResults_to_object(key_words_classifier,int(c),clean_labeled_tweets))


@app.route("/classifier/naiveBayes/<frequency>/<wordsLength>/<uniGrammes>/<biGrammes>/<c>")
def naiveBayes(frequency,wordsLength,uniGrammes,biGrammes,c):

    bayes_classifier = Bayes(bool(strtobool(frequency)),bool(strtobool(uniGrammes)),bool(strtobool(biGrammes)),int(wordsLength))
    
    return json.dumps(classifierResults_to_object(bayes_classifier,int(c),clean_labeled_tweets))



@app.route("/correct", methods=['GET', 'POST'])
def correct_polarity():

    if request.method == 'POST':
        response = request.get_json()
        classify_tweet(response,"data/clean_labeled_tweets.csv")
        return json.dumps({"status" : "ok"})
