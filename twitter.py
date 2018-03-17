from tweet import tweet
from collections import defaultdict


class Twitter:

    def __init__(self):
        self.timelines = defaultdict(list)
        self.relations = defaultdict(set)

    def post_tweet(self, user_id, tweet_id):
        self.timelines[user_id].append(tweet(tweet_id))

    def follow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        self.relations[follower_id].add(followee_id)

    def unfollow(self, follower_id, followee_id):
        if followee_id in self.relations[follower_id]:
            self.relations[follower_id].remove(followee_id)

    def get_feed(self, user_id):
        candidates = []
        candidates += self.timelines[user_id][-10:]
        for followee in self.relations[user_id]:
            candidates += self.timelines[followee][-10:]
        candidates.sort(key=lambda x: x.timestamp, reverse=True)
        return [t.id for t in candidates[-10:]]

    def get_follow(self, user_id):
        return self.relations[user_id]
