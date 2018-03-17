import logging
import http_client
import client


log = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    h_client = http_client.HttpClient('http://localhost:11222')
    follow_client = client.Follow(h_client)
    tweet_client = client.Tweet(h_client)
    feed_client = client.Feed(h_client)
    user_1 = "11"
    user_2 = "22"
    user_3 = "33"
    user_4 = "44"
    # follow test
    assert follow_client.get(user_1)['data'] == []
    follow_client.post(user_1, user_2)
    assert follow_client.get(user_1)['data'] == [user_2]
    follow_client.delete(user_1, user_2)
    assert follow_client.get(user_1)['data'] == []
    follow_client.post(user_1, user_2)
    follow_client.post(user_1, user_3)
    follow_client.post(user_1, user_4)
    assert user_2 in follow_client.get(user_1)['data']
    assert user_3 in follow_client.get(user_1)['data']
    assert user_4 in follow_client.get(user_1)['data']
    # tweet test
    tweet_client.post(user_1, 'tweet1')
    tweet_client.post(user_2, 'tweet2')
    tweet_client.post(user_3, 'tweet3')
    tweet_client.post(user_4, 'tweet4')
    log.info(feed_client.get(user_1))
    log.info(feed_client.get(user_2))
