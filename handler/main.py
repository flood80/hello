#!/usr/bin/env python
#
# Filename:main.py


import tornado.web

import logic

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    #def get_user_locale(self):
    #    return "zh_CN"


class HomeHandler(BaseHandler):
    def get(self):
        entry = logic.User(self.db).validate_user('test', 'test1')
        if not entry:
            print "not found"
        else:
            print str(entry)
        self.render("empty.html")
