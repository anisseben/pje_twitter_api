from Classifier import Classifier
from KNN import KNN
from Bayes import Bayes
from KeyWords import KeyWords
from util import naive_distance
import pandas as pd

clean_labeled_tweets = pd.read_csv("data/clean_labeled_tweets.csv")

fp  = open('corpus/negative.txt')
negative_dict= [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]

fp  = open('corpus/positive.txt')
positive_dict= [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]


"""

# KNN Classifier exemple : 

knn_classifier = KNN(3,naive_distance)


new_tweets = pd.read_csv("data/new_tweets.csv")

new_tweets = knn_classifier.classify_all_tweets(new_tweets,clean_labeled_tweets)

new_tweets.to_csv("data/KNN_labeled_tweets.csv", index=False)

"""
# Naive Bayes Classifier exemple :


bayes_classifier = Bayes(frequency = False ,uni_grammes = False, bi_grammes = False, words_length = 1)



new_tweets2 = pd.read_csv("data/new_tweets.csv")
new_tweets2 = bayes_classifier.classify_all_tweets(new_tweets2,clean_labeled_tweets)


new_tweets2.to_csv("data/Bayes_labeled_tweets.csv", index=False)

"""
# Key Words Classifier exemple :


new_tweets3 = pd.read_csv("data/new_tweets.csv")

key_words_classifier = KeyWords(positive_dict,negative_dict)

new_tweets3 = key_words_classifier.classify_all_tweets(new_tweets3)

new_tweets3.to_csv("data/KeyWords_labeled_tweets.csv", index=False)



# Analyse experimentale Naive Bayes 

bayes_cl1= Bayes(frequency = False ,uni_grammes = True, bi_grammes = False, words_length = 3)

print(bayes_cl1.cross_validation(clean_labeled_tweets,10))

bayes_cl2= Bayes(frequency = False ,uni_grammes = False, bi_grammes = True, words_length = 3)

print(bayes_cl2.cross_validation(clean_labeled_tweets,10))

bayes_cl3= Bayes(frequency = False ,uni_grammes = True, bi_grammes = True, words_length = 3)

print(bayes_cl3.cross_validation(clean_labeled_tweets,10))

bayes_cl4= Bayes(frequency = True ,uni_grammes = True, bi_grammes = False, words_length = 3)

print(bayes_cl4.cross_validation(clean_labeled_tweets,10))

bayes_cl5= Bayes(frequency = True ,uni_grammes = False, bi_grammes = True, words_length = 3)

print(bayes_cl5.cross_validation(clean_labeled_tweets,10))

bayes_cl6= Bayes(frequency = True ,uni_grammes = True, bi_grammes = True, words_length = 3)

print(bayes_cl6.cross_validation(clean_labeled_tweets,10))



# Analyse experimentale Keys words


key_words_cl = KeyWords(positive_dict,negative_dict)


print(key_words_cl.cross_validation(clean_labeled_tweets,5))



# Analyse experimentale KNN


knn_cla = KNN(3,naive_distance)

print(knn_cla.cross_validation(clean_labeled_tweets,4))

"""