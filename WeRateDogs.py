#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import tweepy
import json
import matplotlib.pyplot as plt
import time
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Tweepy keys and token

consumer_key = '****'
consumer_secret = '****'
access_token = '****'
access_secret = '****'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# In[3]:


###1 - Gathering Data

twitter_arch_df = pd.read_csv('twitter-archive-enhanced.csv')


# In[4]:


#requsting the tweets
with open ('image-predictions.tsv','wb') as file:
    img_pred = requests.get('https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv', auth=('user', 'pass'))
    file.write(img_pred.content)


# In[5]:


#open the tsv file
img_pred_df = pd.read_csv('image-predictions.tsv',sep = '\t')


# In[6]:


#Collecting information from Twitter api
collected =[]
not_collected = [] # to avoid the errors because of exception 
with open ('tweet_json.txt','w') as file:
    for twitter_id in list(twitter_arch_df['tweet_id']):
        try:
            tweet_status = api.get_status(twitter_id,tweet_mode='extended')
            json.dump(tweet_status._json, file)
            file.write('\n')
            collected.append(twitter_id)
        except Exception as e:
            not_collected.append(twitter_id)


# In[7]:


tweet_status = pd.read_json('tweet_json.txt', lines= True , encoding = 'utf-8')


# In[8]:


twitter_arch_df.head()


# In[9]:


twitter_arch_df.sample(50)


# In[10]:


img_pred_df


# In[11]:


tweet_status


# In[12]:


twitter_arch_df[twitter_arch_df['rating_denominator'] >15]


# In[13]:


twitter_arch_df[twitter_arch_df['rating_denominator']%4 == 0]


# In[14]:


twitter_arch_df[twitter_arch_df['rating_denominator']%50
                == 0]


# In[15]:


twitter_arch_df.info()


# In[16]:


twitter_arch_df.describe()


# In[17]:


twitter_arch_df[twitter_arch_df['rating_denominator']==0]


# In[18]:


twitter_arch_df[twitter_arch_df['rating_numerator']==0]


# In[19]:


img_pred_df.info()


# In[20]:


img_pred_df.describe()


# In[21]:


tweet_status.info()


# In[22]:


tweet_status.describe()


# Assessment report
# Quality issues in:
# 
# 1- twitter_arch_df:
#     1- there is a lot of missing data.
#     2- Delete the zeroth value in rating_denominator column.
#     3- delete any value in rating_numinator column above (80) 
#     4- delete any value in rating_denominator column above (80)
#     5- No(1254) replace (80 by 10) in denominator column
#     6- No(1254) replace (80 by 10) in numenator column
#     7- No(1433) replace (40 by 10) in numenator column
#     8- No(1433) replace (40 by 10) in denominator column
#     9- No(1202) replace (40 by 10) in numenator column
#     10- No(1202) replace (40 by 10) in denominator column
#     11- No(1274) replace (45 by 15) in numenator column
#     12- No(1274) replace (50 by 10) in denominator column
#     13- No(1351) replace (50 by 10) in denominator column
#     14- No(1274) replace (60 by 10) in numenator column
#     15- Delete the zeroth value in rating_numerator column.
# 
# 
# 2- img_pred_df:
#     1- Missing data
# 
# 
# 3- tweet_status:
#     1- missing data
#     2- I think that we can delete the column of the language because we know that the whole data is in 
#     English.
# 
# Tidness issues:
# 
# * retweets and favorites in their own table (tweets_df)
# * three separate tables
# 
# 
# 1- twitter_arch_df: 
#     1- it's better to make just one column to include the types of the dogs.
#     2- there is a lot of columns that we don't need it in the analysis process like
#         ['retweeted_status_user_id'].
# 
# 
# 2- img_pred_df:
#     1- give the columns which are related to (p1,p2,p3) more describtive names.
# 
# 
# 3- tweet_status:
#     1- delete un-needed data ('columns') in analysis like ['possibly_sensitive']

# Data cleaning
# 
#     here we will solve the issues which we have seen in the data in 
#         the assessmen step.

# In[23]:


# at first we will make copies to work with it 

twitter_arch_clean = twitter_arch_df.copy()
img_pred_clean = img_pred_df.copy()
tweet_status_clean = tweet_status.copy() 


# 1- for tweet_arch_df

# In[24]:


# remove the zeroth value in rating_denominator
x= twitter_arch_clean[twitter_arch_clean['rating_denominator']==0]
twitter_arch_clean.drop(x.index,inplace=True)


# In[25]:


#test
twitter_arch_clean[twitter_arch_clean['rating_denominator']==0]


# In[26]:


# remove the zeroth values in rating_numerator
y = twitter_arch_clean[twitter_arch_clean['rating_numerator']==0]
twitter_arch_clean.drop(y.index,inplace=True)


# In[27]:


#test
twitter_arch_clean[twitter_arch_clean['rating_numerator']==0]


# In[28]:


# remove any rating_numerator>20 
z= twitter_arch_clean[twitter_arch_clean['rating_numerator']>80]
twitter_arch_clean.drop(z.index,inplace=True)


# In[29]:


#test
twitter_arch_clean[twitter_arch_clean['rating_numerator']>80]


# In[30]:


#test for rating_denominator
twitter_arch_clean[twitter_arch_clean['rating_numerator']>80]


# In[31]:


twitter_arch_clean[twitter_arch_clean['rating_numerator']==80]


# In[32]:


twitter_arch_clean['rating_numerator'] = twitter_arch_clean['rating_numerator'].replace(80,10)
twitter_arch_clean[twitter_arch_clean['rating_numerator']==80]


# In[33]:


twitter_arch_clean['rating_numerator'] = twitter_arch_clean['rating_numerator'].replace(40,10)
twitter_arch_clean['rating_numerator'] = twitter_arch_clean['rating_numerator'].replace(50,10)
twitter_arch_clean['rating_numerator'] = twitter_arch_clean['rating_numerator'].replace(45,15)
twitter_arch_clean['rating_numerator'] = twitter_arch_clean['rating_numerator'].replace(60,10)
twitter_arch_clean[twitter_arch_clean['rating_numerator']==45]


# In[34]:


twitter_arch_clean['rating_denominator'] = twitter_arch_clean['rating_denominator'].replace(80,10)
twitter_arch_clean['rating_denominator'] = twitter_arch_clean['rating_denominator'].replace(40,10)
twitter_arch_clean['rating_denominator'] = twitter_arch_clean['rating_denominator'].replace(50,10)

twitter_arch_clean[twitter_arch_clean['rating_denominator']==50]


# In[35]:


#to test that there isn't any values above 20
twitter_arch_clean[twitter_arch_clean['rating_denominator']>20]


# # for tweet_status

# In[36]:


# delete un-needed columns like [ lang]
tweet_status_clean=tweet_status_clean.drop('possibly_sensitive',axis=1)


# In[37]:


#test
tweet_status_clean


# ### Tidness issues cleaning
#   #### merge three datasets in one
# 

# In[38]:


twitter = pd.merge(twitter_arch_clean, img_pred_clean, how = 'left')

#Combine master dataframe with JSON
twitter = pd.merge(twitter, tweet_status, how = 'left')


# In[39]:


twitter.info()


# In[40]:


twitter.head()


# In[41]:


twitter = twitter.drop(['possibly_sensitive','possibly_sensitive_appealable','retweeted_status','quoted_status_id'],axis=1)


# In[42]:


twitter.info()


# In[44]:




twitter.loc[twitter['doggo'] == 'doggo', 'dog_class'] = 'doggo'
twitter.loc[twitter['floofer'] == 'floofer', 'dog_class'] = 'floofer'
twitter.loc[twitter['pupper'] == 'pupper', 'dog_class'] = 'pupper'
twitter.loc[twitter['puppo'] == 'puppo', 'dog_class'] = 'puppo'

twitter = twitter.drop(['doggo', 'floofer', 'pupper', 'puppo'], axis = 1)

twitter.isnull().sum()


# In[45]:


twitter.drop(['in_reply_to_screen_name','in_reply_to_user_id_str','in_reply_to_status_id_str','quoted_status_permalink'
              ,'quoted_status_permalink','quoted_status'],axis=1,inplace=True)
twitter.info()


# In[46]:


twitter.drop(['geo','coordinates','contributors'],axis=1,inplace=True)
twitter.info()


# In[47]:


twitter.drop(['quoted_status_id_str','in_reply_to_user_id','in_reply_to_status_id'],axis=1,inplace=True)


# In[48]:


twitter.drop('place',axis=1,inplace=True)


# In[49]:


twitter_co = twitter.copy()

median_retweet = np.median(twitter_co.retweet_count.dropna())
median_favorite = np.median(twitter_co.favorite_count.dropna())

twitter_co.retweet_count = twitter_co.retweet_count.fillna(median_retweet).astype('int64')
twitter_co.favorite_count = twitter_co.favorite_count.fillna(median_favorite).astype('int64')

twitter_co.dropna(inplace=True)

twitter_co.info()


# # Storing the data

# In[50]:


twitter_co.to_csv('twitter_archive_master.csv', encoding='utf-8', index=False)


# ## Analysis = visualization
# ### 1- Insights
# 

# In[51]:


# the first insight
j = sns.distplot(twitter_co.favorite_count, color = 'red',axlabel = 'Favourite Count')
plt.show()


# In[52]:


# the first insight
j = sns.distplot(twitter_co.favorite_count, color = 'red',axlabel = 'Favourite Count')
plt.show()


# In[53]:


# the Third insight
f= sns.distplot(twitter_co['rating_numerator'],color = 'green',axlabel='Rating Numerator')
plt.show()


# # The visualization

# In[54]:


g = sns.regplot(x=twitter_co.retweet_count, y=twitter_co.favorite_count,scatter_kws={"color": "blue"}, line_kws={"color": "red"})
plt.title("Favorites and Retweets")
plt.xlabel('Retweet')
plt.ylabel('Favorites')
plt.show()

