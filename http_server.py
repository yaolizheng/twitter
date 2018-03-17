import tornado.httpserver
import tornado.ioloop
import tornado.web
import handlers
from twitter import Twitter
import logging

log = logging.getLogger(__name__)


class WebServer:

    def __init__(self, config):
        self.config = config
        self.ioloop = tornado.ioloop.IOLoop.instance()
        twitter = Twitter()
        kwargs = dict(twitter=twitter, config=config)
        self.app = self.make_app(kwargs)
        self.http_server = tornado.httpserver.HTTPServer(self.app)

    def make_app(self, kwargs):
        return tornado.web.Application([
            tornado.web.url(
                handlers.status.Handler.urlspec,
                handlers.status.Handler,
                kwargs
            ),
            tornado.web.url(
                handlers.follow.Handler.urlspec,
                handlers.follow.Handler,
                kwargs
            ),
            tornado.web.url(
                handlers.tweet.Handler.urlspec,
                handlers.tweet.Handler,
                kwargs
            ),
            tornado.web.url(
                handlers.feed.Handler.urlspec,
                handlers.feed.Handler,
                kwargs
            ),
        ])

    def serve(self):
        self.http_server.listen(self.config['port'], self.config['host'])
        self.ioloop.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    config = {'port': 11222, 'host': 'localhost'}
    server = WebServer(config)
    server.serve()
