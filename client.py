import logging
import json

log = logging.getLogger(__name__)


class Follow:

    def __init__(self, client):
        self.client = client
        self.base = ('follow', )

    def get(self, follower):
        path = list(self.base)
        path.extend([follower])
        client = self.client.join(*path)
        return json.loads(client.get().content)

    def post(self, follower, followee):
        path = list(self.base)
        path.extend([follower])
        client = self.client.join(*path)
        data = json.dumps(dict(followee=followee))
        return json.loads(client.post(data=data).content)

    def delete(self, follower, followee):
        path = list(self.base)
        path.extend([follower])
        client = self.client.join(*path)
        data = json.dumps(dict(followee=followee))
        return json.loads(client.delete(data=data).content)


class Feed:

    def __init__(self, client):
        self.client = client
        self.base = ('feed', )

    def get(self, user_id):
        path = list(self.base)
        path.extend([user_id])
        client = self.client.join(*path)
        return json.loads(client.get().content)


class Tweet:

    def __init__(self, client):
        self.client = client
        self.base = ('tweet', )

    def post(self, user_id, tweet):
        path = list(self.base)
        path.extend([user_id])
        client = self.client.join(*path)
        data = json.dumps(dict(tweet=tweet))
        return json.loads(client.post(data=data).content)