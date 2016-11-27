# -*- coding: utf-8 -*-

import re

MIN_PASSWORD_LENGTH = 4

def validate_name(name):
    name_format=u'[a-zA-ZšđčćžŠĐČĆŽ .-]+'
    name_re = re.compile(name_format)
    return name_re.match(name)

def validate_email(email):
    email_format = u'[^@]+@[^@]+\.[^@]+'
    email_re = re.compile(email_format)
    return email_re.match(email)

def validate_password(password):
    if len(password) >= MIN_PASSWORD_LENGTH:
        return True
    return False
