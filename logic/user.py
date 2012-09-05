#!/usr/bin/env python
#
# Filename:user.py


class User(object):
    def __init__(self, db):
        self._db = db


    def validate_user(self, email, password):
        entry = self._db.get("SELECT * FROM users where email='%s'" % email)
        if entry and entry.password == password:
            return entry
