from Classifier import Classifier
import re

class Bayes(Classifier) :
    """
    Naive Bayes Classification class
    """
    def __init__(self, frequency = False ,uni_grammes = False, bi_grammes = False, words_length = 1) :
        """
        create a Naive Bayes classifier
        :param Boll frequency: 
        :param Bool uni_grammes: 
        :param Bool bi_grammes:
        :param int words_length:
        """
        self.frequency = frequency
        self.uni_grammes = uni_grammes
        self.bi_grammes = bi_grammes
        self.words_length = words_length
        
    
    def nbr_word_in_tweet(self,tweet,word):
        """
        calculate the frequency of a word in a tweet
        :param str tweet: a tweet
        :param str word: a word
        :return: int the number of repetition
        """
        
        try :
            return len(re.findall(word, tweet))
        except Exception :
            return 0




    def nbr_words_all_tweets(self,df):
        """
        calculate the number of a words in a all the tweets
        :param pd df: tweets 
        :return: int the number of words
        """
        nbr_words= 0
        for index,value in df.iterrows() :
            nbr_words+= len(value["tweet"].split(" "))
        return nbr_words


    def remove_short_words(self,df):
        """
        filter the words by length
        :param pd df: tweets 
        :return: pd filtred tweets
        """
        for index, tweet in df["tweet"].items() :

            words = filter (lambda word: len(word) > self.words_length, tweet.split())
            df.loc[index, "tweet"] = ' '.join(words)

        return df



    def prob_word_classe(self,tweet_with_polarity,word,N,Nc):
        """
        calculate the probabilty of the word in the class of a specific polarity 
        :param pd tweet_with_polarity: tweet with a specific polarity 
        :param str word: a word
        :param int N: total number of words in all the tweets
        :param int Nc: total number of words in all the tweets with a specific polarity 
        :return: float the probabilty
        """
        nbr_word = 0
        for index,value in tweet_with_polarity.iterrows() :
            nbr_word+= self.nbr_word_in_tweet(value["tweet"],word)
        return (nbr_word+1)/(Nc+N)



    def set_tweet_words(self,tweet):
        """
        return a list of words of a tweet using differents techniques
        :param tweet str: a tweet
        :return list: list of words 
        """
        tweet_words =  tweet.split()
        if self.uni_grammes :
            tweet_words =  tweet.split()
            
        elif self.bi_grammes:
            tweet =  tweet.split()
            tweet_words = list(map(' '.join, zip(tweet[:-1], tweet[1:])))

        elif self.uni_grammes and self.bi_grammes:
            tweet =  tweet.split()
            tweet_words = list(map(' '.join, zip(tweet[:-1], tweet[1:]))) + tweet
            
        return tweet_words


    def prob_tweet_classe(self,df_clean,tweet,polarity):
        """
        calculate the probabilty of a tweet to be with a specific polarity
        :param pd df_clean: clean tweets
        :param str tweet: the tweet
        :param int polarity: a polarity
        :return: float the probabilty
        """
        tweet_with_polarity = df_clean.query("polarity == " + polarity)

        nbr_tweets = df_clean.shape[0]
        nbr_tweets_polarity = tweet_with_polarity.shape[0]

        N = self.nbr_words_all_tweets(df_clean)
        Nc = self.nbr_words_all_tweets(tweet_with_polarity)

        
        tweet_words = self.set_tweet_words(tweet) 
        if self.frequency == False:
            tweet_words = set(tweet_words)

        prob = 1
        for word in tweet_words:
            prob *= self.prob_word_classe(tweet_with_polarity,word,N,Nc)

        return prob * (nbr_tweets_polarity/nbr_tweets)

        
    def evaluate_tweet_polarity_Bayes(self,tweet,df_clean):
        """
        Evaluate the polarity of a tweet using naive Bayes
        :param str tweet: the tweet
        :param pd clean_clean: clean tweets
        :return int: the polarity of the tweet
        """
        polarity_dict = {"0" : self.prob_tweet_classe(df_clean,tweet,"0"), "2" : self.prob_tweet_classe(df_clean,tweet,"2"), "4" : self.prob_tweet_classe(df_clean,tweet,"4")}
        return max(polarity_dict, key=polarity_dict.get)



    def classify_all_tweets(self,new_tweets,clean_tweets):
        """
        Evaluate the polarity of all tweets using naive Bayes with our clean tweets
        :param pd new_tweets: tweets to evaluate
        :param pd clean_tweets: clean tweets
        :return: the new_tweets labeled
        """
        if self.words_length > 1 :
            clean_tweets = self.remove_short_words(clean_tweets)
            new_tweets = self.remove_short_words(new_tweets)

        for index, tweet in new_tweets["tweet"].items() :

            polarity = self.evaluate_tweet_polarity_Bayes(tweet,clean_tweets)
            new_tweets.loc[index, "polarity"] = int(polarity)
        
        return new_tweets

