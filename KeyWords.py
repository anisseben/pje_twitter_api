from Classifier import Classifier
import re

class KeyWords(Classifier):
    """
    Key Words classification
    """
    
    def __init__(self,positive_dict,negative_dict):
        """
        create the Key Words classifier
        :param list positive_dict: corpus of positive words
        :param list negative_dict: corpus of negative words
        """
        self.positive_dict = positive_dict
        self.negative_dict = negative_dict

    
    def calculate_dict_words(self,text,words_list):
        """
        calculate the number of words of tweets present in the words_list
        :param: str text: the tweet
        :param: list words_list: list of words (corpus)
        :return: number of words present in the corpus
        """
        nbr_words = 0
        for word in words_list :
            frequency = len(re.findall(word, text))
            nbr_words += frequency
        return nbr_words



    def classify_all_tweets(self,new_tweets,clean_tweets):
        """
        :param pd new_tweets: clean tweets to label
        :return: pd labeled tweets
        """       
        for index, value in new_tweets["tweet"].items() :

            positive_words = self.calculate_dict_words(value,self.positive_dict)
            negative_words = self.calculate_dict_words(value,self.negative_dict)
            
            if positive_words > negative_words :
                new_tweets.loc[index, "polarity"] = 4
            if positive_words < negative_words :
                new_tweets.loc[index, "polarity"] = 0
            if  negative_words == positive_words :
                new_tweets.loc[index, "polarity"] = 2
            if positive_words == 0 and negative_words == 0:
                new_tweets.loc[index, "polarity"] = 2
            

        return new_tweets
