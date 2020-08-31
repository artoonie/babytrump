import os

import html
import tweepy
import twitter


class TrumpStreamListener(tweepy.StreamListener):
  @classmethod
  def _filter_only_his_tweets(cls, status):
    """ Otherwise we'll get all replies to tweets too """
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    return True

  def on_status(self, status):
    if (self._filter_only_his_tweets(status)):
      print(status.text)

  def on_error(self, status_code):
   if status_code == 420:
     print("Error 420")
     #returning False in on_error disconnects the stream
     return False


class Tweepy():
  def __init__(self):
    api = self._create_api()

  @classmethod
  def _create_api(self):
    auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET_KEY'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)

  @classmethod
  def _create_stream(self, api):
    streamListener = TrumpStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(follow=["25073877"])
    return stream

class PythonTwitter():
  def __init__(self):
    self.api = self._create_api()
    self._restore_last_seen_tweet_id()

  def _create_api(self):
    api = twitter.Api(consumer_key=os.environ['API_KEY'],
                      consumer_secret=os.environ['API_SECRET_KEY'],
                      access_token_key=os.environ['ACCESS_TOKEN'],
                      access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
									    sleep_on_rate_limit=True,
											tweet_mode='extended')
    return api

  def _store_last_seen_id(self, last_seen_tweet_id):
    self.last_seen_tweet_id = last_seen_tweet_id
    print("Saving last tweet id ", last_seen_tweet_id)
    with open('last_seen_tweet_id.txt', 'w') as f:
      f.write(str(last_seen_tweet_id))

  def _restore_last_seen_tweet_id(self):
    try:
      with open('last_seen_tweet_id.txt', 'r') as f:
        self.last_seen_tweet_id = int(f.read())
      print("Restored last tweet ID:", self.last_seen_tweet_id)
    except Exception as e:
      print("Failed to read last seen tweet ID: ", e)
      self.last_seen_tweet_id = None

  def read_stream(self):
    statuses = self.api.GetUserTimeline(user_id='25073877', count=5, exclude_replies=True, since_id=self.last_seen_tweet_id)
    if statuses:
      self._store_last_seen_id(statuses[0].id)
    statuses = [s for s in statuses if not s.retweeted_status]
    statuses = [html.unescape(s.full_text) for s in statuses]
    return statuses

  def tweet(self, tweet):
    try:
        status = self.api.PostUpdate(tweet)
        print("Sent tweet:", tweet)
    except UnicodeDecodeError:
        print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
        raise
