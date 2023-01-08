#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter
import nltk
import pandas as pd
import numpy as np
import plotly


def cleanData(keyword):


    filename_csv  = keyword

    final_filename_csv = "final_"+keyword

    # tweetsData = pd.read_csv("./FinalDataSet.csv" , encoding = "ISO-8859-1")
    tweetsData = pd.read_csv(filename_csv, encoding="ISO-8859-1")

    # In[20]:

    tweetsData.head(5)

    # In[21]:

    plotly.tools.set_credentials_file(username='swmathias', api_key='IUApAvbxLdKWUicRaovv')

    # In[22]:

    # fake = len(tweetsData[tweetsData["Final Label"] == "FAKE"])
    # real = len(tweetsData[tweetsData["Final Label"] == "REAL"])
    # dist = [
    #     graph_objs.Bar(
    #         x=["fake","real"],
    #         y=[fake, real],
    # )]
    # py.plot({"data":dist, "layout":graph_objs.Layout(title="Fake and Real Tweets distribution in training set")})

    # In[23]:

    import re
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    def tokenize(s):
        return tokens_re.findall(s)

    def preproces(s, lowercase=False):
        tokens = tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    # In[24]:

    tweetsData['tokenized_text'] = tweetsData['text'].apply(preproces)

    # In[25]:

    from nltk.corpus import stopwords
    nltk.download('stopwords')

    # In[26]:

    # Removes stopwords
    stop_words = set(stopwords.words('english'))
    tweetsData['token_texts'] = tweetsData['tokenized_text'].apply(
        lambda x: [w for w in x if w.lower() not in stop_words])

    # In[27]:

    tweetsData.head(5)

    # In[28]:

    # function defined to calculate number of occurences of a symbol
    def count_occurences(character, word_array):
        counter = 0
        for j, word in enumerate(word_array):
            for char in word:
                if char == character:
                    counter += 1
        return counter

    # In[29]:

    # calculates number of ?, !, hashtags and mentions
    tweetsData['no_of_question_marks'] = tweetsData['token_texts'].apply(lambda txt: count_occurences("?", txt))
    tweetsData['no_of_exclamation_marks'] = tweetsData['token_texts'].apply(lambda txt: count_occurences("!", txt))
    tweetsData['no_of_hashtags'] = tweetsData['token_texts'].apply(lambda txt: count_occurences("#", txt))
    tweetsData['no_of_mentions'] = tweetsData['token_texts'].apply(lambda txt: count_occurences("@", txt))

    # In[30]:

    def count_by_regex(regex, plain_text):
        return len(re.findall(regex, plain_text))

    # In[45]:

    tweetsData.head(5)

    # In[32]:

    # Calculates number of URLs in a tweet
    tweetsData['no_of_urls'] = tweetsData['text'].apply(lambda txt: count_by_regex("http.?://[^\s]+[\s]?", txt))

    # In[168]:

    # Not working as of now. Need to look at it later if needed
    class EmoticonDetector:
        emoticons = {}

        def __init__(self, emoticon_file="./emoticons.txt"):
            from pathlib import Path
            content = Path(emoticon_file).read_text()
            positive = True
            for line in content.split("\n"):
                if "positive" in line.lower():
                    positive = True
                    continue
                elif "negative" in line.lower():
                    positive = False
                    continue

                self.emoticons[line] = positive

        def is_positive(self, emoticon):
            if emoticon in self.emoticons:
                return self.emoticons[emoticon]
            return False

        def is_emoticon(self, to_check):
            return to_check in self.emoticons

    # In[231]:

    def count_by_lambda(expression, word_array):
        return len(list(filter(expression, word_array)))

    # In[56]:

    # May need this code later. But this code does not work
    # ed = EmoticonDetector()
    # tweetsData['no_of_positive_emoticons'] = tweetsData['text'].apply(lambda txt: count_by_lambda(lambda word: ed.is_emoticon(word) and ed.is_positive(word), txt))

    # In[46]:

    # In[75]:

    # tweetsData['no_of_uppercase_words'] = tweetsData['tokenized_text'].apply(lambda txt: count_by_lambda(lambda word: word == word.upper(),
    #                                                                                          txt))

    # In[34]:

    # Function to Remove URLs and mentions from tweets
    def remove_url_by_regex(pattern, string):
        return re.sub(pattern, "", string)

    # In[35]:

    # Removes URLs
    tweetsData['cleaned_text'] = tweetsData['text'].apply(lambda txt: remove_url_by_regex("http.?://[^\s]+[\s]?", txt))

    # In[36]:

    # Removes mentions
    tweetsData['cleaned_text'] = tweetsData['cleaned_text'].apply(lambda txt: remove_url_by_regex(r'(?:@[\w_]+)', txt))

    # In[209]:

    # strs = "how much for the maple syrup??? $20.99? That's?ricidulous!!!"
    # print(strs)
    # nstr = re.sub(r'[?|$|.|!]',r'',strs)
    # print (nstr)

    # In[37]:

    # Calculates number of colon marks
    tweetsData['no_of_colon_marks'] = tweetsData['cleaned_text'].apply(lambda txt: count_occurences(":", txt))

    # In[236]:

    # Remove punctuation marks
    tweetsData['cleaned_text'] = tweetsData['cleaned_text'].apply(
        lambda txt: remove_url_by_regex(r'[,|:|\|=|&|;|%|$|@|^|*|-|#|?|!|.]', txt))

    # In[44]:

    # Counts number of words
    tweetsData['no_of_words'] = tweetsData['cleaned_text'].apply(lambda txt: len(re.findall(r'\w+', txt)))

    tweetsData['user_has_url?'] = tweetsData['user_url'].apply(lambda x: "Yes" if x else "No")

    # In[ ]:

    tweetsData.to_csv(final_filename_csv)


    return final_filename_csv



