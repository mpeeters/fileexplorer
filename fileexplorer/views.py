# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config

import os

from fileexplorer.explorer import Folder


@view_config(route_name='home',
             renderer='templates/home.pt',
             permission='view')
def home(request):
    return {
        'folder': Folder(request),
    }


@view_config(route_name='file',
             permission='view')
def file(request):
    basepath = request.registry.settings.get('fileexplorer.path')
    filepath = os.path.join(basepath, *request.matchdict.get('path'))
    if os.path.exists(filepath) is False:
        raise HTTPNotFound
    return FileResponse(filepath, request)


@view_config(route_name='folder',
             renderer='templates/home.pt',
             permission='view')
def folder(request):
    return {
        'folder': Folder(request),
    }
