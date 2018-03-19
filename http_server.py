import tornado.httpserver
import tornado.ioloop
import tornado.web
import handlers
from twitter import Twitter
import logging
from db import model
import pylibmc
import json
import argparse


log = logging.getLogger(__name__)


class WebServer:

    def __init__(self, config):
        self.config = config
        self.ioloop = tornado.ioloop.IOLoop.instance()
        mc = pylibmc.Client(self.config['cache'], behaviors={"cas": True})
        twitter = Twitter(mc)
        kwargs = dict(twitter=twitter, config=config)
        self.app = self.make_app(kwargs)
        self.http_server = tornado.httpserver.HTTPServer(self.app)
        db_config = self.config['db']
        model.init_database(
            db_config['address'], db_config['keyspace'],
            db_config['username'], db_config['password'])

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
            tornado.web.url(
                handlers.user.Handler.urlspec,
                handlers.user.Handler,
                kwargs
            ),
        ])

    def serve(self):
        self.http_server.listen(self.config['port'], self.config['host'])
        self.ioloop.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json')
    args = parser.parse_args()
    with open(args.config) as f:
        config = json.load(f)
    log.info(config)
    server = WebServer(config)
    server.serve()
