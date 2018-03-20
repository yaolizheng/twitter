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
            r'/follow'
            r'/(?P<follower>[\w-]+)'
        )

    @gen.coroutine
    def post(self, follower):
        log.info('post follow %s %s' % (follower, self.request.body))
        followee = json.loads(self.request.body)['followee']
        log.info('followee %s' % followee)
        self.twitter.follow(follower, followee)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))

    @gen.coroutine
    def get(self, follower):
        log.info('get follow %s ' % follower)
        self.set_header('Content-Type', 'application/json')
        response = self.response
        response['data'] = self.twitter.get_follow(follower)
        self.finish(json.dumps(response))

    @gen.coroutine
    def delete(self, follower):
        log.info('delete follow %s %s' % (follower, self.request.body))
        followee = json.loads(self.request.body)['followee']
        self.twitter.unfollow(follower, followee)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))
