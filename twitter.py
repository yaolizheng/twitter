from tweet import Tweet
from collections import defaultdict
from cassandra.cqlengine.query import DoesNotExist
from db import model
import time
import logging
from cache import Cache


log = logging.getLogger(__name__)


class Twitter:

    def __init__(self, mc, config):
        self.timelines = defaultdict(list)
        self.relations = defaultdict(set)
        self.tweets_cache = config['tweets_cache']
        self.feed_num = config['feed_num']
        self.relation_cache = Cache(mc, prefix='REL', dup=False)
        self.user_tweet_cache = Cache(
            mc, prefix='TWT', limit=self.tweets_cache)
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
        self.relation_cache.update(follower_id, followee_id)

    def unfollow(self, follower_id, followee_id):
        try:
            model.Relation.get(follower=follower_id, followee=followee_id).delete()
        except DoesNotExist:
            log.info('Relation entry not found %s %s' % (
                follower_id, followee_id))
        self.relation_cache.remove(follower_id, followee_id)

    def get_feed(self, user_id):
        candidates = []
        for user in self.get_follow(user_id) + [user_id]:
            log.info('Search tweets for user %s' % user)
            # try get user top tweets from cache first
            res = self.user_tweet_cache.get(user)
            if res is None:
                candidates += self.get_tweet(
                    user, limit=self.tweets_cache, update_cache=True)
            else:
                log.info('Load tweets from cache for user %s' % user)
                for tweet in res:
                    candidates.append(Tweet(
                        tweet[0], tweet[1], tweet[2], self.tweet_cache))
        # get latest tweets
        candidates.sort(key=lambda x: x.timestamp, reverse=True)
        return [str(c) for c in candidates[:self.feed_num]]

    def get_tweet(self, user_id, limit=None, update_cache=False):
        # read tweets from db
        tweets = sorted(model.Tweet.filter(
            user_id=user_id), key=lambda x: x.time_stamp, reverse=True)
        candidates = []
        cache_list = []
        for i in range(len(tweets)):
            if limit is not None and i > limit:
                break
            tweet = tweets[i]
            log.info('Find tweets %s in db for %s' % (
                tweet.id, tweet.user_id))
            candidates.append(Tweet(
                tweet.id, tweet.user_id, tweet.time_stamp,
                self.tweet_cache))
            cache_list.append((
                tweet.id, tweet.user_id, tweet.time_stamp))
        if update_cache:
            self.user_tweet_cache.set(user_id, cache_list)
        return candidates

    def delete_tweet(self, user_id, tweet_id):
        try:
            tweet = model.Tweet.get(id=tweet_id)
        except DoesNotExist:
            log.warning('Tweet %s not found' % id)
        self.user_tweet_cache.remove(user_id, (
            tweet.id, tweet.user_id, tweet.time_stamp))
        tweet.delete()

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
        try:
            return model.User.get(id=id).name
        except DoesNotExist:
            log.warning('User %s not found' % id)
            return None

    def delete_user(self, id):
        try:
            model.User.get(id=id).delete()
        except DoesNotExist:
            log.warning('User %s not found' % id)
        # delete relation
        for relation in model.Relation.filter(followee=id).allow_filtering():
            self.unfollow(relation.follower, relation.followee)
        for relation in model.Relation.filter(follower=id):
            relation.delete()
        # delete cache
        self.relation_cache.delete(id)
        self.user_tweet_cache.delete(id)
        for tweet in model.Tweet.filter(user_id=id):
            tweet.delete()
