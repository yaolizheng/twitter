import logging
import http_client
import client
import time
from test_utils import generate_tweets


log = logging.getLogger(__name__)


class test:

    def __init__(self):
        h_client = http_client.HttpClient('http://localhost:11222')
        self.follow_client = client.Follow(h_client)
        self.tweet_client = client.Tweet(h_client)
        self.feed_client = client.Feed(h_client)
        self.user_client = client.User(h_client)

    def test_user(self):
        self.user_1 = self.user_client.post('AAA')['data']
        self.user_2 = self.user_client.post('AAA')['data']
        self.user_3 = self.user_client.post('AAA')['data']
        self.user_4 = self.user_client.post('AAA')['data']

    def test_follow(self):
        assert self.follow_client.get(self.user_1)['data'] == []
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
        res = self.feed_client.get(self.user_1)['data']
        print res
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_1, generate_tweets())['data'])
            time.sleep(0.2)
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_2, generate_tweets())['data'])
            time.sleep(0.2)
        res = self.feed_client.get(self.user_1)['data']
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_3, generate_tweets())['data'])
            time.sleep(0.2)
        for i in range(5):
            result.append(
                self.tweet_client.post(self.user_4, generate_tweets())['data'])
            time.sleep(0.2)
        res = self.feed_client.get(self.user_1)['data']
        print res

    def test(self):
        self.test_user()
        self.test_follow()
        self.test_tweet()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test = test()
    test.test()
