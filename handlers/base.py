from tornado import web


class Handler(web.RequestHandler):

    def initialize(self, twitter, config):
        self.twitter = twitter
        self.config = config
        self.response = {'status': 'success'}
