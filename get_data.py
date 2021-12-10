from auth import api,tweepy
import pandas as pd
import csv, re, math



def generate_data(file,query,count):
    """
    generate a csv file using Tweepy api
    :param file str: file path
    :param query str: the subject
    :param count int: number of tweets
    :return None:
    """
    header = ["id",	"user",	"tweet", "date", "polarity"]

    data = [status for status in tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended',lang='fr').items(count)]

    with open(file, 'w', encoding='UTF8') as f1:
        writer = csv.writer(f1)
        # write the header
        writer.writerow(header)
        for tweet in data :
            if hasattr(tweet, "retweeted_status"):
                text = tweet.retweeted_status.full_text
            else:
                text = tweet.full_text

            row = [tweet.id ,tweet.user.name ,text, tweet.created_at, -1]
            # write the data
            writer.writerow(row)



def clean_tweet(text):
    """
    clean a tweet text by removing unuseful strings
    :param text str: the text
    :return str: the cleaned text
    """
    text =  ' '.join(re.sub('([@#][A-Za-z0-9_]+)|(\w+:\/\/\S+)' ,'',text).split())
    text =  ' '.join(re.sub('RT' ,'',text).split())
    text =  ' '.join(re.sub('(?<=\w)([!?,;.])', r' \1',text).split())
    text =  ' '.join(re.sub('\((.+?)\)',r' \1',text).split())
    text =  ' '.join(re.sub(r"[\$]{1}[\d,]+\.?\d{0,2}","$XX",text).split())
    text =  ' '.join(re.sub(r"[\€]{1}[\d,]+\.?\d{0,2}","€XX",text).split())
    text =  ' '.join(re.sub(r"(\+)","\+",text).split())
    text =  ' '.join(re.sub(r"(\*)","\*",text).split())
    text =  ' '.join(re.sub(r"(\?)","\?",text).split())

    return text



def clean_all_tweets(csv_file):
    """
    clean all the tweets texts of the csv_file
    :param csv_file str: file path
    :return None:
    """
    df = pd.read_csv(csv_file)
    
    for index, value in df["tweet"].items() :

        text = clean_tweet(value)
        df.loc[index, "tweet"] = text
    
    df.drop_duplicates(subset=["tweet"], inplace=True)
    df.to_csv(csv_file, index=False)


def search_tweets(query,count):
    """
    search all tweets about a subject using Tweepy
    :query str: the subject
    :count int: number of tweets
    :return pandas dataframe: the tweets cleaned
    """
    generate_data("data/new_tweets.csv",query,count)
    clean_all_tweets("data/new_tweets.csv")
    
    return pd.read_csv("data/new_tweets.csv")


def df_to_object(df_tweets):
    """
    transforme un data frame pandas à une list objet
    :param df_tweet: pandas dataframe 
    :return list: une liste de tweet (objets)
    """
    data = []
    for index, row in df_tweets.iterrows() :

        tweet = {}
        tweet["id"] = row.id
        tweet["tweet"] = row.tweet
        tweet["user"] = row.user
        tweet["date"] = row.date
        tweet["polarity"] = row.polarity

        data.append(tweet)
    
    return data


def classifierResults_to_object(classifier,c,clean_labeled_tweets):

    data = {}
    stats = {}
    new_tweets = pd.read_csv("data/new_tweets.csv")
    classified_tweets = classifier.classify_all_tweets(new_tweets,clean_labeled_tweets)
    score = classifier.cross_validation(clean_labeled_tweets,c)
    stats["score"] = math.trunc(score*100)
    stats["nbr_tweets"] = classified_tweets.shape[0]
    stats["positive_tweets"] = classified_tweets.query("polarity ==4").shape[0]
    stats["negative_tweets"] = classified_tweets.query("polarity ==0").shape[0]
    stats["neutral_tweets"] = classified_tweets.query("polarity ==2").shape[0]
    data["tweets"] = df_to_object(classified_tweets)
    data["stats"] = stats

    return data


def classify_tweet(tweet,file):

    df = pd.read_csv(file)

    if not ((df["id"] == tweet["id"])).any():
        df = df.append(tweet, ignore_index = True)
        df.to_csv(file, index=False)
