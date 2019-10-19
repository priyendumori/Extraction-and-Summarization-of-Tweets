import tweepy
import re
import string
import os

MAX_TWEETS = 200
REQUIRED_TWEETS = 10

CONSUMER_TOKEN = "jHTLoXi1itNEIboVkkG5PlZlM"
CONSUMER_SECRET = "P4GsPqM4ms9amDLdHC69aKXk1gom7NH17apofBCDbMmp2uBgZ5"
ACCESS_TOKEN = "554538683-luV4dNLwBP33ifxIjdCRMljx2wAftj01RcRvjhrI"
ACCESS_TOKEN_SECRET = "kRoBfbr3HBnMKCcXVaPwGtIj8P2Mo2LmgXjw86JI2OOlf"
auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

tweets_folder = "../data/tweets/"

seen = []

def write_to_file(filename, tweet):
	with open(filename, "w") as f: 
		f.write(tweet) 

def get_tweets(hashtag):
	if not os.path.isdir(tweets_folder+hashtag):
		os.mkdir(tweets_folder+hashtag)
	hash_tag_folder = tweets_folder+hashtag
	count=0
	for tweet in tweepy.Cursor(api.search, q="#"+hashtag, lang="en", tweet_mode='extended').items(MAX_TWEETS):
		if 'retweeted_status' in dir(tweet):
			text=tweet.retweeted_status.full_text
		else:
			text=tweet.full_text
		
		if 'in_reply_to_status_id' in dir(tweet):
			if tweet.in_reply_to_status_id != None:
				continue

		try:
			if tweet.entities['media'][0]['type']=='photo':
				continue

			if tweet.entities['media'][0]['type']=='video':
				continue
		except:
			pass

		text = re.sub('&amp;','&',text)
		# text = re.sub(r'[.,"!]+', '', text, flags=re.MULTILINE) # removes the characters specified
		text = re.sub(r'^RT[\s]+', '', text, flags=re.MULTILINE) # removes RT
		text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) #remove link
		text = re.sub(r'[:]+', '', text, flags=re.MULTILINE)	
		text = re.sub(r'[^\x00-\x7F]+','', text)

		new_text = ""		
		for i in text.split(): # remove @ and #words, punctuataion
			if not i.startswith('@') and not i.startswith('#') and i not in string.punctuation:
				new_text+=i+" "	
		text = new_text			
		if len(text)>80:
			if text in seen:
				continue
			else:
				count+=1
				seen.append(text)
				write_to_file(tweets_folder+hashtag+"/"+str(count), text)
		if count>=REQUIRED_TWEETS:
			break

if not os.path.isdir("../data/tweets"):
	os.mkdir("../data/tweets")

print("Enter a hashtag without the hash: ")
print("Example: metoo")
input_hashtag = input()
get_tweets(input_hashtag)