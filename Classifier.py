from abc import ABC, abstractmethod
import functools
import operator
import numpy as np

class Classifier(ABC):
    """
    Classification class
    """
    @abstractmethod
    def classify_all_tweets(self,new_tweets,clean_tweets):
        """
        Evaluate the polarity of all tweets with our clean tweets
        :param pd new_tweets: tweets to evaluate
        :param pd clean_tweets: clean tweets
        :return: the new_tweets labeled
        """
        pass


    def calculate_score(self,df_test,df_train,clean_tweets):

        df_test_res = self.classify_all_tweets(df_test,df_train)
        nbr_test = df_test_res.shape[0]
        wrong_estimations = 0

        for index, value in df_test_res.iterrows() :

            real_polarity = clean_tweets[clean_tweets["id"] == value["id"]].iloc[0]["polarity"]
            
            if str(real_polarity) != str(value["polarity"]) :
                wrong_estimations += 1 

        return wrong_estimations/ nbr_test



    def cross_validation(self,clean_tweets,k):
        
        sets = np.array_split(clean_tweets.index.values, k)
        nbr_folds = len(sets)

        scores = []
        for i in range(nbr_folds):
            
            test_index = sets[i]
            train_index = functools.reduce(operator.iconcat, sets[:i], []) + functools.reduce(operator.iconcat, sets[i+1:], [])

            scores.append(self.calculate_score(clean_tweets.iloc[test_index],clean_tweets.iloc[train_index],clean_tweets))

        scores_sum = np.array(scores).sum()

        return scores_sum/nbr_folds

          


