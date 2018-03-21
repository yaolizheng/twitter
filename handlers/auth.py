import macaroons
import logging
import time

log = logging.getLogger(__name__)

TIME_CAVEAT_PREFIX = 'time < '
NAMESPACE_CAVEAT_PREFIX = 'namespace = '
SECONDS_PER_DAY = 60 * 60 * 24

test_secret = 'test secret'
Unauthorized = macaroons.Unauthorized
MacaroonError = macaroons.MacaroonError

TEST_TOKEN = "MDAxMGxvY2F0aW9uIENBCjAwMTJpZGVudGlmaWVyIENBCjAwMmZzaWduYXR1cmUgvhnXB9jOTE5S9NGZfmWVP1xQ-gU5h_79kb6E7ftnvkkK"


def generate_token(
        location,
        secret=None,
        identifier=None,
        expires=None):

    if secret is None:
        log.warning('No secret specified, using insecure test secret')
        secret = test_secret
    if identifier is None:
        identifier = location

    m = macaroons.create(location, secret, identifier)

    if expires is None:
        log.warning('Token will never expire since no expire time specified')
    else:
        delta = expires - time.time()
        if delta < 0:
            log.warning('Expiration time %s occurs in the past', expires)
        m = m.add_first_party_caveat(TIME_CAVEAT_PREFIX + str(expires))

    log.debug('auth token generated:\n%s', m.inspect())

    return m.serialize()


def verify_token(token, secret=test_secret):
    m = macaroons.deserialize(token)
    v = macaroons.Verifier()
    v.satisfy_general(check_time)
    return v.verify(m, secret)


def check_time(caveat):
    fresh = False
    if caveat.startswith(TIME_CAVEAT_PREFIX):
        try:
            timestr = caveat[len(TIME_CAVEAT_PREFIX):]
            expires = float(timestr)
            fresh = expires > time.time()
        except ValueError:
            log.exception('Malformed caveat %s', repr(caveat))
    return fresh


if __name__ == '__main__':
    token = generate_token('CA')
    print verify_token(token)
