# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from passlib.apache import HtpasswdFile
from pyramid.security import Allow


USERS = []
GROUPS = {}


def load_users(filepath):
    pwd_file = HtpasswdFile(filepath)
    for user in pwd_file.users():
        USERS.append(user)
    return pwd_file


def add_users_groups(groups):
    for value in groups:
        if not value:
            continue
        user, group = value.split(':')
        add_user_group(user, 'group:{0}'.format(group))


def add_user_group(login, group):
    if login not in GROUPS:
        GROUPS[login] = []
    if group not in GROUPS[login]:
        GROUPS[login].append(group)


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])


def check_password(request, login, password):
    pwd_file = request.registry.settings.get('fileexplorer.users')
    return pwd_file.check_password(login, password)


class FileExplorer(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
        (Allow, 'group:viewers', 'view'),
    ]

    def __init__(self, request):
        self.request = request
