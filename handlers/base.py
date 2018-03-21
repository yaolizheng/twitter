from tornado import web
import auth
import logging
import httplib

log = logging.getLogger(__name__)


class Handler(web.RequestHandler):

    def initialize(self, twitter, config):
        self.twitter = twitter
        self.config = config
        self.response = {'status': 'success'}

    def get_token(self):
        try:
            return self.request.headers["Auth-Token"]
        except KeyError:
            return None

    def authorized(self):
        token = self.get_token()
        if token is None:
            log.error("Request not authorized, no token provided")
            return False
        try:
            result = auth.verify_token(token)
        except Exception:
            log.exception("Request not authorized, exception raised")
            return False
        return result

    def check_authorized(self):
        if not self.authorized():
            raise web.HTTPError(httplib.UNAUTHORIZED)
