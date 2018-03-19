import logging
import random
import http_client
import client
import time
from test_utils import generate_tweets
import json


log = logging.getLogger(__name__)


class FunctionalTest:

    def __init__(self, url):
        h_client = http_client.HttpClient(url)
        self.follow_client = client.Follow(h_client)
        self.tweet_client = client.Tweet(h_client)
        self.feed_client = client.Feed(h_client)
        self.user_client = client.User(h_client)

    def test_user(self):
        self.user_1 = self.user_client.post('test_user')['data']
        self.user_2 = self.user_client.post('test_user')['data']
        self.user_3 = self.user_client.post('test_user')['data']
        self.user_4 = self.user_client.post('test_user')['data']

    def test_follow(self):
        assert self.follow_client.get(self.user_4)['data'] == []
        self.follow_client.post(self.user_1, self.user_2)
        self.follow_client.post(self.user_1, self.user_2)
        assert self.user_2 in self.follow_client.get(self.user_1)['data']
        self.follow_client.delete(self.user_1, self.user_2)
        assert self.follow_client.get(self.user_1)['data'] == []
        self.follow_client.post(self.user_1, self.user_2)
        self.follow_client.post(self.user_1, self.user_3)
        self.follow_client.post(self.user_1, self.user_4)
        follows = self.follow_client.get(self.user_1)['data']
        assert self.user_2 in follows
        assert self.user_3 in follows
        assert self.user_4 in follows

    def test_tweet(self):
        result = []
        assert self.feed_client.get(self.user_1)['data'] == []
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_1, generate_tweets())['data'])
            time.sleep(1)
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_2, generate_tweets())['data'])
            time.sleep(1)
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_3, generate_tweets())['data'])
            time.sleep(1)
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_4, generate_tweets())['data'])
            time.sleep(1)
        res = self.feed_client.get(self.user_1)['data']
        assert [json.loads(x)['id'] for x in res] == result[::-1][:10]

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

    def test_follow(self, user, num):
        options = {
            'follow': self.follow_client.post,
            'unfollow': self.follow_client.delete,
            'get_follow': self.follow_client.get}
        for i in range(num):
            follower = random.choice(user)
            followee = random.choice(user)
            function = random.choice(options.keys())
            if function == 'get_follow':
                options[function](follower)['data']
            else:
                options[function](follower, followee)

    def test(self):
        user = self.test_user(10)
        self.test_follow(user, 100)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # url = "http://52.32.47.169:11222"
    url = "http://localhost:11222"
    # test = FunctionalTest(url)
    test = ScaleTest(url)
    test.test()
