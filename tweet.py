from db import model
import uuid
import datetime
import json
import logging

log = logging.getLogger(__name__)


class Tweet:

    def __init__(self, id, user_id, timestamp, tweet_cache):
        self.id = str(id)
        self.user_id = str(user_id)
        self.timestamp = str(datetime.datetime.utcfromtimestamp(
            int(timestamp)))
        self.tweet_cache = tweet_cache

    def __repr__(self):
        data = dict(
            id=self.id, user=self.user_id,
            timestamp=self.timestamp, content=self.get_tweet_content())
        return json.dumps(data)

    def get_tweet_content(self):
        res = self.tweet_cache.get(self.id)
        if res is None:
            tweet = model.Tweet.get(id=uuid.UUID(self.id))
            self.tweet_cache.get(self.id, tweet)
            res = tweet.content
        else:
            log.info('Get tweet %s from cache' % self.id)
        return res
