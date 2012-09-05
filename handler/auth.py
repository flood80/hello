#!/usr/bin/env python
#
# Filename:auth.py

import tornado.web
import logic
import lib


from main import BaseHandler


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")


    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        entry = logic.User(self.db).validate_user(email, password)
        if not entry:
            self.render("login.html")
        else:
            self.set_secure_cookie("user", str(user.id))
            self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class WeiboLoginHandler(tornado.web.RequestHandler, lib.auth.WeiboMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri = 'http://yourong.org/callback',
                client_id = '2715148932', #self.settings["facebook_api_key"],
                client_secret = '7231e761010bcfb1b1d71bd0eeb78d7c', #self.settings["facebook_secret"],
                code = self.get_argument("code"),
                callback = self.async_callback(
                    self._on_login))
            return
        self.authorize_redirect(redirect_uri='http://yourong.org/callback',
                                client_id='2715148932')


    def _on_login(self, user):
        if not user:
            self.render("login.html")
        else:
            self.set_secure_cookie("user", str(user["id"]))
            self.redirect(self.get_argument("next", "/"))


class WeiboLogintHandler(tornado.web.RequestHandler):
    def get(self):
        APP_KEY = '2715148932' # app key
        APP_SECRET = '7231e761010bcfb1b1d71bd0eeb78d7c' # app secret
        CALLBACK_URL = 'http://yourong.org/callback' # callback url
        client = lib.weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        if self.get_argument("code", False):
            code = self.get_argument("code")
            r = client.request_access_token(code)
            access_token = r.access_token
            expires_in = r.expires_in
            self.redirect('/?t=%s&e=%s' % (access_token, expires_in))
        url = client.get_authorize_url()
        print url
        self.redirect(url)
