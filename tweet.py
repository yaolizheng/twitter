from db import model
import uuid
import datetime
import json


class Tweet:

    def __init__(self, id, user_id, timestamp):
        self.id = str(id)
        self.user_id = str(user_id)
        self.timestamp = str(datetime.datetime.utcfromtimestamp(
            int(timestamp)))

    def __repr__(self):
        data = dict(
            id=self.id, user=self.user_id,
            timestamp=self.timestamp, content=self.get_tweet_content())
        return json.dumps(data)

    def get_tweet_content(self):
        return model.Tweet.get(id=uuid.UUID(self.id)).content
