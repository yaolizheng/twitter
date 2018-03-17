from __future__ import absolute_import

import logging
import requests
import urlparse


log = logging.getLogger(__name__)


HTTPError = requests.exceptions.HTTPError


class HttpClient(object):

    def __init__(self, url, secure=None, cert=None):
        self._url = url
        self._secure = secure
        self._cert = cert

    @property
    def url(self):
        return self._url

    def join(self, *args):
        if not args:
            return self
        url = self.absurl(list(args))
        return HttpClient(url, secure=self._secure, cert=self._cert)

    def absurl(self, path):
        url = urlparse.urlsplit(self._url, scheme="http")
        assert url.fragment == ""
        assert url.query == ""
        abspath = "/".join([url.path] + path)
        return urlparse.urlunsplit(
            (url.scheme,
             url.netloc,
             abspath,
             url.query,
             url.fragment))

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request("PATCH", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)

    def request(self, method, path=[], client_auth=True, **kwargs):
        if not self._secure:
            kwargs['verify'] = False
        else:
            kwargs['verify'] = self._secure
        if self._cert is not None and client_auth is True:
            kwargs['cert'] = self._cert
        if client_auth is False:
            log.debug("Skipping client authentication")
        return self._make_request(method, path, **kwargs)

    def _make_request(self, method, path=[], **kwargs):
        url = self.absurl(path)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise
        if (
            "Content-Length" in response.headers and
            int(response.headers["Content-Length"]) !=
            len(response.content)
        ):
            log.error("Get bad content length")
            raise HTTPError("Bad content length")
        return response
