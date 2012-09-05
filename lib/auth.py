#!/usr/bin/env python
#
# Filename:auth.py

import tornado.auth
import logging
import urllib

from tornado import httpclient
from tornado import escape

class WeiboMixin(tornado.auth.OAuth2Mixin):
    """Facebook authentication using the new Graph API and OAuth2."""
    _OAUTH_ACCESS_TOKEN_URL = "https://api.weibo.com/oauth2/access_token"
    _OAUTH_AUTHORIZE_URL = "https://api.weibo.com/oauth2/authorize?"
    _OAUTH_NO_CALLBACKS = False

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                              code, callback, extra_fields=None):
        http = httpclient.AsyncHTTPClient()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            }

        fields = set(['id', 'name', 'location', 'profile_image_url', 'url'])
        if extra_fields: fields.update(extra_fields)
        http.fetch(self._OAUTH_ACCESS_TOKEN_URL, callback=self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, fields), method="POST", body=urllib.urlencode(args))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                        callback, fields, response):
        if response.error:
            logging.warning('Weibo auth error: %s' % str(response))
            callback(None)
            return

        session = escape.json_decode(response.body)
        self.weibo_request(
            path="/2/users/show.json",
            callback=self.async_callback(
                self._on_get_user_info, callback, session, fields),
            access_token=session["access_token"],
            uid=session["uid"]
            )


    def _on_get_user_info(self, callback, session, fields, user):
        if user is None:
            callback(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update({"access_token": session["access_token"], "session_expires": session.get("expires")})
        callback(fieldmap)

    def weibo_request(self, path, callback, access_token=None,
                           post_args=None, **args):
        url = "https://api.weibo.com" + path
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
            all_args.update(post_args or {})
        if all_args: url += "?" + urllib.urlencode(all_args)
        callback = self.async_callback(self._on_weibo_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="GET", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_weibo_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(escape.json_decode(response.body))
