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
        self.check_authorized()
        log.info('post user %s' % self.request.body)
        name = json.loads(self.request.body)['name']
        response = self.response
        response['data'] = str(self.twitter.add_user(name))
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(response))

    @gen.coroutine
    def delete(self):
        self.check_authorized()
        log.info('delete user %s' % self.request.body)
        id = json.loads(self.request.body)['id']
        self.twitter.delete_user(id)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(self.response))

    @gen.coroutine
    def get(self):
        self.check_authorized()
        id = self.get_argument('id', None)
        log.info('get user %s' % id)
        response = self.response
        response['data'] = self.twitter.get_user(id)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(response))
