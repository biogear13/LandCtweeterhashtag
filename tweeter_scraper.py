import configparser
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import time
# get tokens
config = configparser.ConfigParser()
config.read('configfile.ini')
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
# authenticate
auth = tweepy.OAuth2AppHandler(api_key, api_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
def get_tweets_dataframe(working_df, tweets, hashtag):
    #working_df=working_df.drop_duplicates()
    index=len(working_df)
    for tweet in tweets: 
        working_df.loc[index,'tweet_id']=tweet.id
        working_df.loc[index,'created_at']=tweet.created_at
        working_df.loc[index,'user']=tweet.user.screen_name
        working_df.loc[index,'full_text']=tweet.full_text
        working_df.loc[index,'favorite_count']=tweet.favorite_count
        working_df.loc[index,'retweet_count']=tweet.retweet_count
        working_df.loc[index,'hashtags']=hashtag
        print(working_df.loc[index,'created_at'])
        #working_df=working_df.drop_duplicates()
        index+=1
        working_df.to_csv(f'tweeterhashtags/{hashtag}.csv', index=False)
        #time.sleep(1)
    working_df=working_df.drop_duplicates()
    working_df.to_csv(f'tweeterhashtags/{hashtag}.csv', index=False)               
    return working_df
hashtagsweek1 = ['#FridayNightatPortlandRow', '#HauntedWatchParty', '#WatchPartyatPortlandRow', '#HauntedbyaType3','#TogetherForLockwoodandCo','#PrimeForLockwoodandCo','#BringBackLockwoodandCo']
hashtagsweek2 = ['#GhostHuntersWatchParty', '#DisneyForLockwoodandCo', '#BBCforLockwoodandCo', '#AppleTVforLockwoodandCo', '#PrimeForLockwoodandCo', '#JustRecklessEnough']
hashtagsweek3 = ['#LockwoodGhostAuditions', '#ParamountForLockwoodandCo', '#ScullandCo','#RapiersReady', '#CaringforCarlyle', '#DEPRACisOnTheWay', '#BunsForBunchurch']
hashtagsweek4 = ['#CompleteFictionAppreciation', '#DisneySaveLockwood', '#ArtistryofLockwoodandCo', '#ParamountSaveLockwood', '#GhostStrike', '#LockwoodParallelFandoms', '#JustRecklessEnough']
hashtagsall = hashtagsweek1+hashtagsweek2+hashtagsweek3+hashtagsweek4
hashtagsall = list(set(hashtagsall))
hashtagsallp1 = hashtagsall + ['#SaveLockwoodandCo']
hashtags=['#ArtistryofLockwoodandCo']
for hashtag in hashtags:
    print(hashtag)
    try:
        working_df=pd.read_csv(f'tweeterhashtags/{hashtag}.csv')
        #working_df = pd.read_csv('tweeterhashtags/#SkullandCo.csv')
        print(len(working_df))
    except:
        working_df=pd.DataFrame(columns=['tweet_id','created_at', 'user', 'full_text','favorite_count','retweet_count','hashtags'])
    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, tweet_mode='extended').items()
    working_df = get_tweets_dataframe(working_df, tweets, hashtag)
    working_df=working_df.drop_duplicates()
    print(len(working_df))
    time.sleep(60)
    working_df['created_at'] = pd.to_datetime(working_df['created_at'], utc=True)
    # Group the DataFrame by day
    grouped_df = working_df.groupby(pd.Grouper(key='created_at', freq='D'))

    # Calculate the count of rows for each day
    count_per_day = grouped_df['hashtags'].count()

    # Display the count per day
    print(count_per_day)
working_df=pd.DataFrame()
for hashtag in hashtagsall:
    try:
        working_df=pd.concat([working_df, pd.read_csv(f'tweeterhashtags/{hashtag}.csv')], ignore_index=True)
    except:
        pass
working_df['full_text'] = working_df['full_text'].str.replace(r'"', '')
# Create a new column 'retweet' with default value False
working_df['retweet'] = False

# Check if 'full_text' starts with 'RT ' and set 'retweet' column accordingly
working_df.loc[working_df['full_text'].str.startswith('RT '), 'retweet'] = True

working_df['retweet'].value_counts()
import hashlib
# Create a hash function to generate anonymized values
def anonymize(value):
    # Convert the value to a string and hash it using SHA256 algorithm
    hashed_value = hashlib.sha256(str(value).encode()).hexdigest()
    # Take the first 8 characters of the hash as the anonymized value
    anonymized_value = hashed_value[:8]
    return anonymized_value
if 'anonymized_user' in working_df.columns:
    working_df.drop('anonymized_user', axis=1, inplace=True)
user_df = pd.DataFrame(working_df['user'].unique(), columns=['user'])
user_df['anonymized_user'] = user_df['user'].apply(anonymize)
working_df = working_df.merge(user_df, on='user', how='left')

working_df['created_date'] = pd.to_datetime(working_df['created_at'], utc=True)
working_df['week_number'] = working_df['created_date'].dt.isocalendar().week
working_df['week_number'].value_counts()
def get_week_label(week_number):
    if week_number == 20:
        return 'week1'
    elif week_number == 21:
        return 'week2'
    elif week_number == 22:
        return 'week3'
    elif week_number == 23:
        return 'week4'
    else:
        return 'week0'
working_df['week_label'] = working_df['week_number'].apply(get_week_label)
working_df.to_csv('tweeterhashtags/tweets.csv', index=False)
