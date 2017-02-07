# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2016 by NetExpe SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from fileexplorer.security import FileExplorer
from fileexplorer.security import add_users_groups
from fileexplorer.security import groupfinder
from fileexplorer.security import load_users
from fileexplorer.security import load_permissions


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    authn_policy = AuthTktAuthenticationPolicy(
        'secret',
        callback=groupfinder,
        hashalg='sha512',
    )
    authz_policy = ACLAuthorizationPolicy()

    user_file = load_users(settings.get('fileexplorer.htpasswd'))
    settings['fileexplorer.users'] = user_file
    add_users_groups(settings.get('fileexplorer.groups').splitlines())

    load_permissions(settings.get('fileexplorer.permissions'))

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory=FileExplorer,
    )

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('font', 'font', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('file', '/file/*path')
    config.add_route('folder', '/f/*path')

    config.scan()
    return config.make_wsgi_app()
