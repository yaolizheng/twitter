from tweet import Tweet
from collections import defaultdict
from db import model
import time
import logging
from cache import Cache


log = logging.getLogger(__name__)


class Twitter:

    def __init__(self, mc):
        self.timelines = defaultdict(list)
        self.relations = defaultdict(set)
        self.relation_cache = Cache(mc, prefix='REL-')
        self.user_tweet_cache = Cache(mc, prefix='TWT-', limit=10)
        self.tweet_cache = Cache(mc)

    def post_tweet(self, user_id, tweet):
        kwargs = {
            'user_id': user_id, 'content': tweet,
            'time_stamp': str(int(time.time()))}
        tweet_db = model.Tweet.create(**kwargs)
        # update user's top tweets
        self.user_tweet_cache.update(user_id, (
            tweet_db.id, tweet_db.user_id, tweet_db.time_stamp))
        # cache tweets
        self.tweet_cache.set(str(tweet_db.id), tweet)
        return tweet_db.id

    def follow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        kwargs = {'follower': follower_id, 'followee': followee_id}
        model.Relation.create(**kwargs)
        # update cached relations
        self.relation_cache.update(follower_id, followee_id)

    def unfollow(self, follower_id, followee_id):
        model.Relation.get(follower=follower_id, followee=followee_id).delete()
        self.relation_cache.remove(follower_id, followee_id)

    def get_feed(self, user_id):
        candidates = []
        for user in self.get_follow(user_id) + [user_id]:
            log.info('Search tweets for user %s' % user)
            # try get user top tweets from cache first
            res = self.user_tweet_cache.get(user)
            if res is None:
                tweets = sorted(model.Tweet.filter(
                    user_id=user), key=lambda x: x.time_stamp,
                    reverse=True)[:10]
                cache_list = []
                for tweet in tweets:
                    log.info('Find tweets %s in db for %s' % (
                        tweet.id, tweet.user_id))
                    candidates.append(Tweet(
                        tweet.id, tweet.user_id, tweet.time_stamp,
                        self.tweet_cache))
                    cache_list.append((
                        tweet.id, tweet.user_id, tweet.time_stamp))
                # cache user top tweets
                self.user_tweet_cache.set(user, cache_list)
            else:
                log.info('Load tweets from cache for user %s' % user)
                for tweet in res:
                    candidates.append(Tweet(
                        tweet[0], tweet[1], tweet[2], self.tweet_cache))
        # get latest tweets
        candidates.sort(key=lambda x: x.timestamp, reverse=True)
        return [str(c) for c in candidates[-10:]]

    def get_follow(self, user_id):
        res = self.relation_cache.get(user_id)
        if res is None:
            res = [str(x.followee) for x in model.Relation.filter(
                follower=user_id)]
            self.relation_cache.set(user_id, res)
        else:
            log.info('Get follow from cache for user %s' % user_id)
        return res

    def add_user(self, name):
        kwargs = {'name': name}
        return model.User.create(**kwargs).id

    def get_user(self, id):
        return model.User.get(id=id).name
