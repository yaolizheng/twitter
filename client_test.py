import logging
import timer
import random
import http_client
import client
import time
from test_utils import generate_tweets
import json
import concurrent.futures


log = logging.getLogger(__name__)


def test_log(msg):
    log.info('----------%s----------' % msg)


class FunctionalTest:

    def __init__(self, url):
        h_client = http_client.HttpClient(url)
        self.follow_client = client.Follow(h_client)
        self.tweet_client = client.Tweet(h_client)
        self.feed_client = client.Feed(h_client)
        self.user_client = client.User(h_client)

    def test_user(self):
        test_log('Add user1')
        self.user_1 = self.user_client.post('test_user')['data']
        test_log('Add user2')
        self.user_2 = self.user_client.post('test_user')['data']
        test_log('Add user3')
        self.user_3 = self.user_client.post('test_user')['data']
        test_log('Add user4')
        self.user_4 = self.user_client.post('test_user')['data']
        test_log('Get user4')
        test_log('Test user4 is valid')
        assert self.user_client.get(self.user_4)['data'] is not None
        test_log('Delete user4')
        self.user_client.delete(self.user_4)
        time.sleep(2)
        test_log('Get user4')
        test_log('Test user4 is gone')
        assert self.user_client.get(self.user_4)['data'] is None
        test_log('Re-add user4')
        self.user_4 = self.user_client.post('test_user')['data']

    def test_follow(self):
        test_log('Get follower for user4')
        test_log('Test feeds for user4 is empty')
        assert self.follow_client.get(self.user_4)['data'] == []
        test_log('User1 follows user2')
        self.follow_client.post(self.user_1, self.user_2)
        test_log('User1 follows user2')
        self.follow_client.post(self.user_1, self.user_2)
        test_log('Get followee for user1')
        test_log('Test user1 follows user2')
        assert self.user_2 in self.follow_client.get(self.user_1)['data']
        test_log('User1 unfollow user2')
        self.follow_client.delete(self.user_1, self.user_2)
        test_log('Get followee for user1')
        test_log('Test user1 unfollows user2')
        assert self.follow_client.get(self.user_1)['data'] == []
        test_log('User1 follows user2')
        self.follow_client.post(self.user_1, self.user_2)
        test_log('User1 follows user3')
        self.follow_client.post(self.user_1, self.user_3)
        test_log('User1 follows user4')
        self.follow_client.post(self.user_1, self.user_4)
        test_log('Get followee for user1')
        follows = self.follow_client.get(self.user_1)['data']
        test_log('Test user1 follows user2, user3, user4')
        assert self.user_2 in follows
        assert self.user_3 in follows
        assert self.user_4 in follows

    def test_tweet(self):
        result = []
        contents = []
        delete_test = None
        test_log('Get feeds for user1')
        test_log('Test feeds for user1 is empty')
        assert self.feed_client.get(self.user_1)['data'] == []
        test_log('User1 post tweets')
        for i in range(5):
            content = generate_tweets()
            result.append(
                self.tweet_client.post(self.user_1, content)['data'])
            contents.append(content)
            time.sleep(1)
        test_log('Get feeds for user1')
        res = self.tweet_client.get(self.user_1)['data']
        test_log('Test feeds for user1 are correct')
        assert [json.loads(x)['id'] for x in res] == result[::-1]
        assert [json.loads(x)['content'] for x in res] == contents[::-1]
        test_log('User2 post tweets')
        for i in range(5):
            content = generate_tweets()
            result.append(
                self.tweet_client.post(self.user_2, content)['data'])
            contents.append(content)
            time.sleep(1)
        test_log('User3 post tweets')
        for i in range(5):
            content = generate_tweets()
            res = self.tweet_client.post(self.user_3, content)['data']
            contents.append(content)
            delete_test = (self.user_3, res)
            result.append(res)
            time.sleep(1)
        test_log('User4 post tweets')
        for i in range(5):
            content = generate_tweets()
            result.append(
                self.tweet_client.post(self.user_4, content)['data'])
            contents.append(content)
            time.sleep(1)
        time.sleep(1)
        test_log('Get feeds for user1')
        res = self.feed_client.get(self.user_1)['data']
        assert [json.loads(x)['id'] for x in res] == result[::-1][:10]
        assert [json.loads(x)['content'] for x in res] == contents[::-1][:10]
        test_log('Delete user4')
        self.user_client.delete(self.user_4)
        test_log('Get feeds for user1')
        res = self.feed_client.get(self.user_1)['data']
        test_log('Test feeds for user1 are correct')
        assert [json.loads(x)['id'] for x in res] == result[::-1][5:15]
        assert [json.loads(x)['content'] for x in res] == contents[::-1][5:15]
        assert delete_test[1] in [json.loads(x)['id'] for x in res]
        test_log('Delete latest tweet for user3')
        self.tweet_client.delete(delete_test[0], delete_test[1])
        test_log('Get feeds for user1')
        res = self.tweet_client.get(self.user_1)['data']
        test_log('Test deleted feed not in feeds for user1')
        assert delete_test[1] not in [json.loads(x)['id'] for x in res]

    def test(self):
        self.test_user()
        self.test_follow()
        self.test_tweet()


class ScaleTest:

    def __init__(self, url):
        h_client = http_client.HttpClient(url)
        self.follow_client = client.Follow(h_client)
        self.tweet_client = client.Tweet(h_client)
        self.feed_client = client.Feed(h_client)
        self.user_client = client.User(h_client)

    def test_user(self, num):
        user_list = []
        for i in range(num):
            user_list.append(self.user_client.post('test_user')['data'])
        return user_list

    def test_follow(self, user, timeout=60):
        options = {
            'follow': self.follow_client.post,
            'unfollow': self.follow_client.delete,
            'get_follow': self.follow_client.get}
        with timer.Timer() as _elapsed:
            while True:
                if _elapsed.seconds() > timeout:
                    break
                follower = random.choice(user)
                followee = random.choice(user)
                function = random.choice(options.keys())
                if function == 'get_follow':
                    options[function](follower)['data']
                else:
                    options[function](follower, followee)

    def test_tweet(self, user, timeout=60):
        options = {
            'post_tweet': self.tweet_client.post,
            'get_feed': self.feed_client.get}
        with timer.Timer() as _elapsed:
            while True:
                if _elapsed.seconds() > timeout:
                    break
                user_id = random.choice(user)
                function = random.choice(options.keys())
                if function == 'post_tweet':
                    options[function](user_id, generate_tweets())
                else:
                    options[function](user_id)

    def test(self):
        user = self.test_user(100)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future = []
            for i in range(5):
                future.append(executor.submit(self.test_follow, user, 600))
            for i in range(5):
                future.append(executor.submit(self.test_tweet, user, 600))
            for future in concurrent.futures.as_completed(future):
                try:
                    future.result()
                except:
                    raise
