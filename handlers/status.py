from tornado import gen
import props
import base


class Handler(base.Handler):

    @props.classproperty
    def urlspec(cls):
        return r'/status'

    @gen.coroutine
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write("ok")
