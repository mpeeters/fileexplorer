# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2016 by NetExpe SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config

import os

from fileexplorer import utils
from fileexplorer.explorer import Folder


@view_config(route_name='home',
             renderer='templates/home.pt',
             permission='view')
def home(request):
    return {
        'folder': Folder(request),
    }


@view_config(route_name='file',
             permission='can_view')
def file(request):
    filepath = utils.get_path(request)
    if os.path.exists(filepath) is False:
        raise HTTPNotFound
    return FileResponse(filepath, request)


@view_config(route_name='folder',
             renderer='templates/home.pt',
             permission='can_view')
def folder(request):
    return {
        'folder': Folder(request),
    }
