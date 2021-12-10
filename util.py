from Levenshtein import distance as levenshtein_distance


def naive_distance(tweet1,tweet2):
    """
    calculate distance betweet two tweets
    :param tweet1 str: 
    :param tweet2 str: 
    :return int: the distance 
    """
    nbr_total_mots = len(tweet1)+len(tweet2) 
    l_tweet1 = tweet1.split(" ")
    l_tweet2 = tweet2.split(" ")
    mots_communs = len(list(set(l_tweet1)&set(l_tweet2)))
    return (nbr_total_mots - mots_communs)/nbr_total_mots