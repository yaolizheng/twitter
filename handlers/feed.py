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
            r'/feed'
            r'/(?P<user_id>[\w-]+)'
        )

    @gen.coroutine
    def get(self, user_id):
        log.info('get %s ' % user_id)
        self.set_header('Content-Type', 'application/json')
        response = self.response
        response['data'] = self.twitter.get_feed(user_id)
        self.finish(json.dumps(response))
