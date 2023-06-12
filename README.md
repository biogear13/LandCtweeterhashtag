# Lockwood and Co Twitter Hashtag Scraper
## Introduction
This project is a Twitter hashtag scraper that retrieves tweets based on specified hashtags and saves them to CSV files. It utilizes the Tweepy library to interact with the Twitter API.

## Objectives
The objectives of this project are:
- Retrieve tweets containing specific hashtags
- Store the tweets in CSV files for further analysis

## How it Works
1. The project uses the Tweepy library to authenticate and interact with the Twitter API.
2. It reads the API keys and secrets from a configuration file (`configfile.ini`).
3. The `get_tweets_dataframe()` function retrieves tweets for a specific hashtag and saves them to a DataFrame.
4. The collected tweets are then stored in CSV files based on the hashtag.
5. The project also performs data preprocessing tasks, such as removing duplicate tweets and anonymizing user information.
6. Finally, it categorizes the tweets based on the week they were posted and saves the processed data to a `tweets.csv` file.

## Required Libraries
The following libraries are required to run this project:
- configparser
- tweepy
- pandas
- numpy
- datetime
- time
- hashlib

You can install the dependencies by running the following command:
pip install -r requirements.txt


## Setup
1. Clone the repository:

   git clone https://github.com/biogear13/LandCtweeterhashtag.git
   cd your-repository

2. Install the required libraries as mentioned in the previous section.
3. Obtain Twitter API keys and secrets and update them in the `configfile.ini` file.
4. Run the `scraper.py` script:

   python scraper.py


## Scraping and Output
The project scrapes tweets based on the specified hashtags and saves them in CSV files. It also performs data preprocessing tasks and categorizes the tweets based on the week they were posted. The processed data is then saved to the `tweets.csv` file.

For more details on the implementation, please refer to the source code.
