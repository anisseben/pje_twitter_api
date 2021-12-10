from Classifier import Classifier


class KNN(Classifier) :
    """
    KNN Classification class
    """
    def __init__(self,k,distance) :
        """
        create a KNN classifier
        :param int k: KNN coefficient
        :param function distance: calculate a distance between two tweets
        """
        self.k = k
        self.distance = distance


    def evaluate_polarity_KNN(self,tweet,clean_tweets):
        """
        Evaluate the polarity of a tweet using KNN with our clean tweets
        :param str tweet: the tweet
        :param pd clean_tweets: clean tweets
        :return: the plarity of the tweet
        """

        proches_voisins = clean_tweets[0:self.k]
        all_tweets = clean_tweets[self.k+1:]
        
        for index1,value1 in all_tweets.iterrows() :

            distance1 = self.distance(value1["tweet"],tweet)
            for index2, value2  in proches_voisins.iterrows() :
                distance2 = self.distance(value2["tweet"],tweet) 
                if distance1 < distance2 :
                    proches_voisins.loc[index2, "tweet"] = value1["tweet"]
                    proches_voisins.loc[index2, "polarity"] = value1["polarity"]

        return proches_voisins["polarity"].value_counts().idxmax()



    def classify_all_tweets(self,new_tweets,clean_tweets):
        """
        Evaluate the polarity of all tweets using KNN with our clean tweets
        :param pd new_tweets: tweets to evaluate
        :param pd clean_tweets: clean tweets
        :return: the new_tweets labeled
        """
        for index, tweet in new_tweets["tweet"].items() :

            polarity = self.evaluate_polarity_KNN(tweet,clean_tweets)
            new_tweets.loc[index, "polarity"] = polarity
        
        return new_tweets
