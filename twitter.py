from tweet import Tweet
from collections import defaultdict
from db import model
import time
import logging

log = logging.getLogger(__name__)


class Twitter:

    def __init__(self):
        self.timelines = defaultdict(list)
        self.relations = defaultdict(set)

    def post_tweet(self, user_id, tweet):
        kwargs = {
            'user_id': user_id, 'content': tweet,
            'time_stamp': str(int(time.time()))}
        return model.Tweet.create(**kwargs).id

    def follow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        kwargs = {'follower': follower_id, 'followee': followee_id}
        model.Relation.create(**kwargs)

    def unfollow(self, follower_id, followee_id):
        model.Relation.get(follower=follower_id, followee=followee_id).delete()

    def get_feed(self, user_id):
        candidates = []
        for user in self.get_follow(user_id) + [user_id]:
            log.info('Search tweets for %s' % user)
            tweets = sorted(model.Tweet.filter(
                user_id=user), key=lambda x: x.time_stamp, reverse=True)[:10]
            for tweet in tweets:
                log.info('Find tweets %s for %s' % (tweet.id, tweet.user_id))
                candidates.append(Tweet(tweet.id, tweet.user_id, tweet.time_stamp))
        candidates.sort(key=lambda x: x.timestamp, reverse=True)
        return [str(c) for c in candidates[-10:]]

    def get_follow(self, user_id):
        return [str(x.followee) for x in model.Relation.filter(follower=user_id)]

    def add_user(self, name):
        kwargs = {'name': name}
        return model.User.create(**kwargs).id

    def get_user(self, id):
        return model.User.get(id=id).name
