import configparser
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import time

# Get tokens
config = configparser.ConfigParser()
config.read('configfile.ini')
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

# Authenticate
auth = tweepy.OAuth2AppHandler(api_key, api_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_tweets_dataframe(working_df, tweets, hashtag):
    # Increment index using length of working_df
    index = len(working_df)
    for tweet in tweets:
        # Assign values directly to the DataFrame columns
        working_df.loc[index, ['tweet_id', 'created_at', 'user', 'full_text', 'favorite_count', 'retweet_count', 'hashtags']] = tweet.id, tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.favorite_count, tweet.retweet_count, hashtag
        
        # Save DataFrame to CSV after each iteration
        working_df.to_csv(f'tweeterhashtags/{hashtag}.csv', index=False)
        
        index += 1
    
    # Remove duplicates and save to CSV again
    working_df.drop_duplicates().to_csv(f'tweeterhashtags/{hashtag}.csv', index=False)
    
    return working_df

hashtagsweek1 = ['#FridayNightatPortlandRow', '#HauntedWatchParty', '#WatchPartyatPortlandRow', '#HauntedbyaType3', '#TogetherForLockwoodandCo', '#PrimeForLockwoodandCo', '#BringBackLockwoodandCo']
hashtagsweek2 = ['#GhostHuntersWatchParty', '#DisneyForLockwoodandCo', '#BBCforLockwoodandCo', '#AppleTVforLockwoodandCo', '#PrimeForLockwoodandCo', '#JustRecklessEnough']
hashtagsweek3 = ['#LockwoodGhostAuditions', '#ParamountForLockwoodandCo', '#ScullandCo', '#RapiersReady', '#CaringforCarlyle', '#DEPRACisOnTheWay', '#BunsForBunchurch']
hashtagsweek4 = ['#CompleteFictionAppreciation', '#DisneySaveLockwood', '#ArtistryofLockwoodandCo', '#ParamountSaveLockwood', '#GhostStrike', '#LockwoodParallelFandoms', '#JustRecklessEnough']
hashtagsweek5 = ['#StroudsAppreciation' '#VoteLockwoodforNFA', '#PrimeSaveLockwood', '#ScreamingStaircase', '#DEPRACrollcall', '#LivingforLockwood', '#RapiersReady']

# Combine all hashtags into a single list
hashtagsall = list(set(hashtagsweek1 + hashtagsweek2 + hashtagsweek3 + hashtagsweek4))
hashtagonceaweek = hashtagsall +['#SaveLockwoodandCo']

# Create an empty DataFrame to store the tweets
working_df = pd.DataFrame()


# Get tweets that contain the phrase 'Lockwood and Co'
phrase = 'Lockwood and Co'
try:
    working_df = pd.read_csv(f'tweeterhashtags/{phrase}.csv')
    print(len(working_df))
except:
    working_df = pd.DataFrame(columns=['tweet_id', 'created_at', 'user', 'full_text', 'favorite_count', 'retweet_count', 'hashtags'])
    
tweets = tweepy.Cursor(api.search_tweets, q=phrase, tweet_mode='extended').items()
working_df = get_tweets_dataframe(working_df, tweets, phrase)
    
working_df.drop_duplicates(inplace=True)
print(len(working_df))
    
time.sleep(60)
    
working_df['created_at'] = pd.to_datetime(working_df['created_at'], utc=True)
grouped_df = working_df.groupby(pd.Grouper(key='created_at', freq='D'))
count_per_day = grouped_df['hashtags'].count()
print(count_per_day)

ind_hashtag = ['ScullanCo']
# Loop through each hashtag
for hashtag in hashtagonceaweek:
    print(hashtag)
    try:
        working_df = pd.read_csv(f'tweeterhashtags/{hashtag}.csv')
        print(len(working_df))
    except:
        working_df = pd.DataFrame(columns=['tweet_id', 'created_at', 'user', 'full_text', 'favorite_count', 'retweet_count', 'hashtags'])
    
    tweets = tweepy.Cursor(api.search_tweets, q=hashtag, tweet_mode='extended').items()
    working_df = get_tweets_dataframe(working_df, tweets, hashtag)
    
    working_df.drop_duplicates(inplace=True)
    print(len(working_df))
    
    time.sleep(60)
    
    working_df['created_at'] = pd.to_datetime(working_df['created_at'], utc=True)
    grouped_df = working_df.groupby(pd.Grouper(key='created_at', freq='D'))
    count_per_day = grouped_df['hashtags'].count()
    print(count_per_day)

working_df = pd.DataFrame()

for hashtag in hashtagsall:
    try:
        working_df = pd.concat([working_df, pd.read_csv(f'tweeterhashtags/{hashtag}.csv')], ignore_index=True)
    except:
        pass

working_df['full_text'] = working_df['full_text'].str.replace(r'"', '')

working_df['retweet'] = False
working_df.loc[working_df['full_text'].str.startswith('RT '), 'retweet'] = True
print(working_df['retweet'].value_counts())

import hashlib

def anonymize(value):
    hashed_value = hashlib.sha256(str(value).encode()).hexdigest()
    anonymized_value = hashed_value[:8]
    return anonymized_value

if 'anonymized_user' in working_df.columns:
    working_df.drop('anonymized_user', axis=1, inplace=True)

user_df = pd.DataFrame(working_df['user'].unique(), columns=['user'])
user_df['anonymized_user'] = user_df['user'].apply(anonymize)
working_df = working_df.merge(user_df, on='user', how='left')

working_df['created_date'] = pd.to_datetime(working_df['created_at'], utc=True)
working_df['week_number'] = working_df['created_date'].dt.isocalendar().week

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
