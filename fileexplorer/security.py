# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2016 by NetExpe SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from passlib.apache import HtpasswdFile
from pyramid.security import Allow
from pyramid.security import unauthenticated_userid

from fileexplorer import utils


USERS = []
GROUPS = {}
PERMISSIONS = {}


def load_users(filepath):
    pwd_file = HtpasswdFile(filepath)
    for user in pwd_file.users():
        USERS.append(user)
    return pwd_file


def load_permissions(filepath):
    with open(filepath, 'r') as f:
        for permission in f:
            add_permission(*permission.split(':'))


def add_permission(user, folder):
    if user not in PERMISSIONS:
        PERMISSIONS[user] = []
    PERMISSIONS[user].append(folder.strip())


def check_permission(request, path):
    """Ensure that the given user can access to the given path"""
    path = extract_path(request, path)
    # All users can access to root folder
    if path == u'/':
        return True
    user = unauthenticated_userid(request)
    for permission_path in PERMISSIONS.get(user, []):
        if path.startswith(permission_path):
            return True
    return False


def extract_path(request, path):
    """Return the absolute path from a given complete path en system"""
    system_path = request.registry.settings.get('fileexplorer.path')
    path = path.replace(system_path, '')
    if not path:
        path = '/'
    return path


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

    def __init__(self, request):
        self.request = request

    @property
    def __acl__(self):
        acl = [(Allow, 'group:viewers', 'view')]
        path = utils.get_path(self.request)
        if check_permission(self.request, path) is True:
            acl.append([Allow, 'group:viewers', 'can_view'])
        return acl
