# TO DO:
#	1. Clean up
print('RUNNING...')
#################################################################################
import tweepy #V4.12.1 
import configparser #V5.3.0
import pandas as pd #V1.5.1
import csv #V1.0
import datetime
from datetime import date
import pytz # for converting naive datetime to aware #V2022.6
import time
import random
import sys

# Read configs files for twitter.api authorisation
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['consumer_api_key']
api_key_secret = config['twitter']['consumer_api_secret_key']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Time Window in which to collect tweets
#   Startdate - This is set to correspond with the date the WHO was informed of a cluster of cases 
#   of pneumonia with unknown cause in Wuhan that would spark the COVID-19 Pandemic.
start_time_OG = datetime.datetime(2019, 12, 31) #yyyy/mm/dd
start_time = pytz.UTC.localize(start_time_OG)

#   Enddate - can be adjusted accordingly
end_time = date.today()
#end_time = datetime.datetime(2020, 6, 1)
#end_time = pytz.UTC.localize(end_time)


# Load in twitter accounts to be mined
list_of_users = pd.read_csv('Twitter.COG-UK_handles.csv')

# Remove @ symbol from handles and convert to a list
list_of_users['Twitter Handler'] = list_of_users['Twitter Handler'].map(lambda x: x.lstrip('@').rstrip('\n'))
TwitterHandles_list = list_of_users['Twitter Handler'].tolist()
TwitterHandles_list = list(dict.fromkeys(TwitterHandles_list)) # removes duplicates (probably more elegant way to do this with csv to dictionary)

number_users = len(TwitterHandles_list)
user_number = 0

missing_users = []


for userID in TwitterHandles_list:
    
	print('extracting tweets from @' + userID + ': User ' + str(user_number) + ' of ' + str(number_users))
	
    # Extract all (in reality only the latest 3200) tweets from User's timeline
	tweets = tweepy.Cursor(api.user_timeline, screen_name = userID, include_rts=True, tweet_mode = 'extended')
	
    # User's tweets are saved to a list
	list_of_user_tweets = []

	# Columns names for the resultant dataframe are defined
	columns = [
	'tweet_id',
	'user_name', 
	'user_id', 
	'user_handle',
	'created_at',
	'full_text',
	'hashtags',
	'user_mentions',
	'attached_media',
	'reply_to_user',
	'reply_to_tweet_id',
	'reply_to_text',
	'retweet', 
	'retweet_user', 
	'retweeted_tweet_id', 
	'retweet_text',
	'retweet_created_at',
	'user_location',
	'user_description',
	'followers_count',
	'friends_count',
	'time_zone',
	'verified',
	'witheld_in',
	'geo', 
	'coordinates', 
	'place', 
	'contributors', 
	'retweet_count', 
	'favorite_count', 
	'possibly_sensitive', 
	'lang'
	]

	try:

		tweet_n = 0 # Current tweet number
		tweets_in_timeframe = 0
		
		for tweet in tweets.items():

			sys.stdout.write("\r loading tweet: " + str(tweet_n))
			
			if tweet.created_at > start_time:

				tweets_in_timeframe = tweets_in_timeframe + 1

				attributes = list(tweet._json.keys())

				# Extract User attributes
				user_id = tweet.user.id
				user_name = tweet.user.name
				user_handle= tweet.user.screen_name
				user_location = tweet.user.location
				user_description = tweet.user.description
				followers_count = tweet.user.followers_count
				friends_count = tweet.user.friends_count
				time_zone = tweet.user.time_zone
				verified = tweet.user.verified
				witheld_in = ' '.join(map(str,tweet.user.withheld_in_countries))

				# Extract tweet attributes
				created_at = tweet.created_at 
				text = tweet.full_text

				# If tweet is a retweet or quote tweet, relevant attributes are extracted
				if 'retweeted_status' in attributes:
					retweet = 'RT'
					try:
						retweet_user = tweet.retweeted_status.user.screen_name
						retweet_text = tweet.retweeted_status.full_text
						retweeted_tweet_id = tweet.retweeted_status.id_str
						retweet_created_at = tweet.retweeted_status.created_at
					except:
						retweet_user = 'AttributeError'
						retweet_text = None
						retweeted_tweet_id = None
						retweet_created_at = None
				elif tweet.is_quote_status == True:
					retweet = 'QT'
					try:
						retweet_user = tweet.quoted_status.user.screen_name
						retweet_text = tweet.quoted_status.full_text
						retweet_created_at = tweet.quoted_status.created_at
						retweeted_tweet_id = tweet.quoted_status_id_str
					except:
						retweet_user = 'AttributeError'
						retweet_text = None
						retweet_created_at = None
						retweeted_tweet_id = None 
				else:
					retweet = None
					retweet_text = None
					retweet_created_at = None
					retweeted_tweet_id = None
					retweet_user = None

				# Extract entities: hashtags, user_mentions, attached_media
				entities = tweet.entities

				hashtags = entities.get('hashtags')

				hashtag_str = ''
				for i in range(len(hashtags)):
					hashtag = hashtags[i].get('text')
					hashtag_str = hashtag_str + '#' + hashtag + ' '
				hashtag_str = hashtag_str.rstrip()

				user_mentions = entities.get('user_mentions')
				screen_names = ''
				for i in range(len(user_mentions)):
					screen_id_name = user_mentions[i].get('id_str') + '@' + user_mentions[i].get('screen_name')
					screen_names = screen_names + screen_id_name + ' | '
					#screen_names = screen_names.join(map(screen_id_name + ' '))
				screen_names = screen_names[:len(screen_names) - 3]
				
				try:
					media = entities.get('media')
					media_types = ''
					for i in range(len(media)):
						media_type = media[i].get('type')
						media_url = media[i].get('media_url_https')
						media_types = media_type + ':' + media_url + ' '
				except:
					media_types = None

				# Extract reply attributes
				if tweet.in_reply_to_status_id != None:
					reply_to_user = '@' + tweet.in_reply_to_screen_name
					reply_to_tweet_id = tweet.in_reply_to_status_id_str
					try:
						reply_text = api.get_status(tweet.in_reply_to_status_id, tweet_mode = "extended").full_text
					except:
						reply_text = 'tweepy.errors.NotFound: 404 Not Found'
				else:
					reply_to_user = None
					reply_to_tweet_id = None
					reply_text = None
				
				# Extract additional tweet attributes
				geo = tweet.geo
				coordinates = tweet.coordinates
				place = tweet.place
				contributors = tweet.contributors
				retweet_count = tweet.retweet_count
				favorite_count = tweet.favorite_count

				if 'possibly_sensitive' in attributes:
					possibly_sensitive = tweet.possibly_sensitive
					#print(possibly_sensitive)
				else:
					possibly_sensitive = None # change to false?
				lang = tweet.lang

				# Current tweet is added to list_of_user_tweets
				list_of_user_tweets.append([tweet.id, user_name, user_id, user_handle, created_at, text, hashtag_str, screen_names, media_types, reply_to_user, reply_to_tweet_id, reply_text, retweet, retweet_user, retweeted_tweet_id, retweet_text, retweet_created_at, user_location, user_description, followers_count, friends_count, time_zone, verified, witheld_in, geo, coordinates, place, contributors, retweet_count, favorite_count, possibly_sensitive, lang])

				sys.stdout.flush()

			tweet_n = tweet_n + 1
			total_user_tweets = tweet_n

		# list_of_user_tweets is converted to a dataframe
		df_of_user_tweets = pd.DataFrame(list_of_user_tweets, columns = columns)
		print(df_of_user_tweets)

		# User's tweets are saved to a TSV file under Their username
		filename = userID + '_' + str(start_time_OG)[0:10] + 'to' + str(end_time) + '.tsv'
		filepath = 'downloaded_tweets/' + filename
		df_of_user_tweets.to_csv(filepath, sep = '\t')

		print('successfully saved ' + str(tweets_in_timeframe) + '/' + str(total_user_tweets) + ' tweets as' + filename)


		# It seems that only the latest ~3200 tweets on a timeline can be extracted using tweepy, 
        # thus, for some users the algorithm was not able to stretch to the beginning of the 
        # COVID-19 pandemic
		if tweets_in_timeframe == total_user_tweets:
			print("WARNING: User's timeline may be too large to capture")
			print('oldest tweet at: ' + str(created_at))

        # Sleep for some time to avoid overloading the Twitter servers
		wait_time = random.randint(150, 500) # wait between 2 and a half to 5 minutes
		print('sleeping ' + str(wait_time) + ' seconds')
		time.sleep(wait_time)
			    
	# If a user is not found, Their usernames will be displayed
	except:
			print('Problem accessing tweets from ' + userID)
			missing_users += [userID]
    		
	user_number = user_number + 1

if missing_users != []:     
	print('Users not saved')
	print(missing_users)