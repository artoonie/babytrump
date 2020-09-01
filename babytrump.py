import os

from apiWrapper import ApiWrapper
import html
import traceback

class TwitterBabyMonitor():
  def __init__(self):
    self.api = self._create_api()

  def _create_api(self):
    api = ApiWrapper(consumer_key=os.environ['API_KEY'],
                     consumer_secret=os.environ['API_SECRET_KEY'],
                     access_token_key=os.environ['ACCESS_TOKEN'],
                     access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
                     sleep_on_rate_limit=True,
                     tweet_mode='extended')
    return api

  def _store_last_seen_id(self, last_seen_tweet_id):
    me = '1296902986850074628'
    dm = self.api.PostDirectMessage(last_seen_tweet_id, me, return_json=True)

    print("Saved last tweet id ", last_seen_tweet_id, dm)

  def _get_last_seen_tweet_id(self):
    try:
      # Get the last message sent
      last_sent_messages = self.api.GetSentDirectMessages(count=1, return_json=True)
      message_create = last_sent_messages['events'][0]['message_create']
      text = message_create['message_data']['text']
      recipient = message_create['target']['recipient_id']
      sender = message_create['sender_id']

      # Ensure the sender and receiver were both from bb
      assert recipient == sender

      # Store it!
      return int(text)
    except Exception as e:
      print("Failed to read last seen tweet ID")
      traceback.print_exc()
      return None

  def read_stream(self):
    last_seen_tweet_id = self._get_last_seen_tweet_id()
    statuses = self.api.GetUserTimeline(user_id='25073877', count=5, exclude_replies=True, since_id=last_seen_tweet_id)
    statuses = [s for s in statuses if not s.retweeted_status]
    if statuses:
      print(statuses)
      self._store_last_seen_id(statuses[0].id)
    statuses = [html.unescape(s.full_text) for s in statuses]
    return statuses

  def tweet(self, tweet):
    try:
        status = self.api.PostUpdate(tweet)
        print("Sent tweet:", tweet)
    except UnicodeDecodeError:
        print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
        raise
