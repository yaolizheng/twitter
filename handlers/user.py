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
            r'/user'
        )

    @gen.coroutine
    def post(self):
        log.info('post %s' % self.request.body)
        name = json.loads(self.request.body)['name']
        log.info('name %s' % name)
        response = self.response
        response['data'] = str(self.twitter.add_user(name))
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))
