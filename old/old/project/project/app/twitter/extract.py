#!/usr/bin/env python
# coding: utf-8

# In[25]:


import tweepy
from tweepy import OAuthHandler
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import numpy as np


def getTweets(tweetkeyword):
    pd.options.display.max_columns = 50
    pd.options.display.max_rows = 50
    pd.options.display.width = 120

    # consumer_key = '2CF0SjF91irHA3xzSRJwhMiJF'
    # consumer_secret = 'ERNMd3a05M39IZgK1B8C6VeIfFauFMxvfY17LxiTD9omlNha0K'
    # access_token = '908720407682875393-DkzbECIw8z6Alp3axpLgv3njJ1zcjAU'
    # access_secret = 'ZMcWhoSNdYFUwT8aItpYrIg95cGJgYD2zfjerxhqfsstu'

    # consumer_key = 'x6oyrFcPMgSPTB9KXJQAKO5SF'
    # consumer_secret = '007DkU6A8RU5K0BRGZKWOP2xwPmNb5k1Yk8lbeoDK05IP4oZ9P'
    # access_token = '1454025693331800064-PgVHn8SIvzuTOzkNoUQIMQknXja0Qm'
    # access_secret = 'DJoAqclPF7gyyVYKA5HhJGK7FXYkHxqin62hgg2tqbXZ9'

    consumer_key,consumer_secret = 'XE5F8IGwN4LSwlM2oKdlRftk7','F2xBRiWlliyc1yLTHD8s3E5gJeXZBFYYC1H9oWIFaa1Tk716mG'
    access_token,access_secret = '1004136301573099520-NG78DBmsrpnyDU2C8lRk7j9hMnbnt3','151xLtzobJo8O3uma9Z80uylyXPJB0ARaLzMZLjm5rGIW'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    csv_filename = tweetkeyword+".csv"
    # In[26]:

    # Extract 50 tweets based on the keyword
    results = []
    i = 0
    # API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
    # for tweet in tweepy.Cursor(api.search, q=tweetkeyword, lang="en").items():
    print("hobobo")
    userID = tweetkeyword.split("@")[1].split("·")[0].strip()
    # print(api.user_timeline(screen_name=userID,
    #                        # 200 is the maximum allowed count
    #                        count=5,
    #                        include_rts = False,
    #                        # Necessary to keep full_text
    #                        # otherwise only the first 140 words are extracted
    #                        tweet_mode = 'extended'
    #                        ))

    tweets = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=20,
                               include_rts=False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )

    for tweet in tweets:
        #print(tweet)
        tweet.text = tweet.full_text
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            results.append(tweet)
            print(tweet.text)
            print("Scraping  Tweets From Twitter")
            id = tweet.id
            i = i + 1
            print(i)
            # if i==20:
            #     break
    # print(results)

        # print("ID: {}".format(info.id))
        # print(info.created_at)
        # print(info.full_text)
        # print("\n")

    # for tweet in tweepy.Cursor(api.search,count=1, q=tweetkeyword, lang="en").items():
    #     print(tweet)
    #     if (not tweet.retweeted) and ('RT @' not in tweet.text):
    #         results.append(tweet)
    #         print(tweet.text)
    #         print("Scraping  Tweets From Twitter")
    #         id = tweet.id
    #         i = i + 1
    #         print(i)
    #         if i==20:
    #             break
    # print(len(results))

    # In[27]:

    # Store the tweets in a dataframe
    def process_results(results):
        id_list = [tweet.id for tweet in results]
        data_set = pd.DataFrame(id_list, columns=["id"])

        # Processing Tweet Data

        data_set["text"] = [tweet.text for tweet in results]  # text of tweet
        data_set["created_at"] = [tweet.created_at for tweet in results]  # when the tweet was created
        data_set["retweet_count"] = [tweet.retweet_count for tweet in results]  # number of retweets
        data_set["favorite_count"] = [tweet.favorite_count for tweet in results]  # number of favourites
        data_set["source"] = [tweet.source for tweet in results]  # source of the tweet
        data_set["length"] = [len(tweet.text) for tweet in results]  # number of characters in tweet

        # Processing User Data
        data_set["user_id"] = [tweet.author.id for tweet in results]  # id of the author
        data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
        data_set["user_name"] = [tweet.author.name for tweet in results]
        data_set["user_created_at"] = [tweet.author.created_at for tweet in results]  # age of user account
        data_set["user_description"] = [tweet.author.description for tweet in results]
        data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]  # number of followers
        data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]  # number of followers

        data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results]  # number of friends
        data_set["user_location"] = [tweet.author.location for tweet in results]  # user has a location in profile?
        data_set["user_statuses_count"] = [tweet.author.statuses_count for tweet in results]  # number of statuses
        data_set["user_verified"] = [tweet.author.verified for tweet in results]  # user is verified?
        data_set["user_url"] = [tweet.author.url for tweet in results]  # user has a URL?

        return data_set

    data_set = process_results(results)

    # In[28]:

    # Save the dataframe in a csv
    data_set.to_csv(csv_filename, index=False, encoding='utf-8')

    # In[29]:

    df = pd.read_csv(csv_filename)

    # In[30]:

    df

    # In[8]:

    df.dtypes

    # In[9]:

    df["number_of_QuestionMarks"] = ""

    # In[10]:

    df

    # In[11]:

    # df["user_has_url?"] = ""

    # In[12]:

    df["user_has_url?"] = np.where(df["user_url"].isnull(), 'No', 'Yes')

    # In[13]:

    df

    # In[ ]:

    data_set.to_csv(csv_filename, index=False, encoding='utf-8')

    return data_set.iloc[0]
    # return csv_filename
