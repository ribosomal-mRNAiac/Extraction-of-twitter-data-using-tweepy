# Extraction of tweets from COG-UK November 2022
**In light of events at Twitter in November 2022 and fear of the loss of historical evidence, this script was written for [WhatIsBiotechnology](https://www.whatisbiotechnology.org/index.php/), using tools from the Python library [Tweepy](https://docs.tweepy.org/en/stable/api.html)[^1], to extract tweets posted by members of the [COVID-19 Genomics UK Consortium](https://www.cogconsortium.uk/)[^2] from the beginning of the COVID-19 pandemic.**

The script also includes:
- a config file, in which the access keys and tokens needed for a User to access the Twitter API are stated.
- a CSV file containg the handles of the Twitter Users desired to be extracted.

Attributes from the tweet status items outputted by the tweepy command are compiled and outputted into a TSV file for each individual Twitter User with columns corresponding to:
- the tweet id number
- the User's name 
- the User's twitter id number
- the User's twitter handle
- the date and time at which each tweet was created
- the full text of each tweet
- hashtags included in the tweet
- other twitter users mentioned in the tweet
- the type and hyperlinks to any media included in the tweet
- whether the tweet was in reply to another Twitter User
- the id number of any original tweet the User's tweet was in reply to
- the full text of any original tweet the User's tweet was in reply to
- whether the User's tweet was a retweet (RT for retweet, QT for quote tweets) 
- the handle of the user retweeted 
- the id number of the original tweet retweeted
- the full text of the original tweet retweeted
- the the date and time at which the original tweet retweeted was created
- the location of the Twitter User
- the Twitter User's twitter bio
- the number of followers the Twitter User has (at time of extraction)
- the number of friends the Twitter User has (at time of extraction)
- the time zone in which the tweet was posted
- the verification status of the Twitter User (many of the COG-UK members would have held verified accounts during the COVID-19 pandemic and at time of posting, but this will have been affected at the time of extraction due to the new Twitter verification system)
- whether the user is witheld in any countries
- the [geo-tag status](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/geo) of the tweet
- the coordinates at which a tweet was posted 
- the (place) location at which a tweet was posted
- other contributors to the tweet
- the number of retweets a tweet recieved 
- the number of likes(favourites) a tweet recieved
- whether the tweet was flagged by Twitter as possibly sensitive 
- the language in which the tweet was posted

## Future use
This tool was able to run in November 2022, but cannot be guaranteed to be compatible with Twitter systems in the future.

[^1]: Roesslein, J. (2020). Tweepy: Twitter for Python! https://github.com/Tweepy/Tweepy
[^2]: The COVID-19 Genomics UK (COG-UK) consortium. (2020). An integrated national scale SARS-CoV-2 genomic surveillance network. The Lancet Microbe, 1(03), e99–e100. https://doi.org/10.1016/s2666-5247(20)30054-9  
