import base
import props
import logging
from tornado import gen
import json

log = logging.getLogger(__name__)


class Handler(base.Handler):

    @props.classproperty
    def urlspec(cls):
        return (
            r'/tweet'
            r'/(?P<user_id>[\w-]+)'
        )

    @gen.coroutine
    def post(self, user_id):
        log.info('post tweet %s %s' % (user_id, self.request.body))
        tweet = json.loads(self.request.body)['tweet']
        response = self.response
        response['data'] = str(self.twitter.post_tweet(user_id, tweet))
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(response))

    @gen.coroutine
    def get(self, user_id):
        log.info('get tweet %s' % user_id)
        response = self.response
        response['data'] = [str(x) for x in self.twitter.get_tweet(user_id)]
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(response))

    @gen.coroutine
    def delete(self, user_id):
        log.info('delete tweet %s %s' % (user_id, self.request.body))
        tweet = json.loads(self.request.body)['tweet']
        self.twitter.delete_tweet(user_id, tweet)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))
