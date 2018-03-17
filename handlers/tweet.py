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
        log.info('post %s %s' % (user_id, self.request.body))
        tweet = json.loads(self.request.body)['tweet']
        log.info('tweet %s' % tweet)
        self.twitter.post_tweet(user_id, tweet)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))
