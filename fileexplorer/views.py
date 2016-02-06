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


@view_config(route_name='home',
             renderer='templates/home.pt',
             permission='view')
def home(request):
    basepath = request.registry.settings.get('fileexplorer.path')
    return {
        'files': get_file_list(basepath),
        'parent': '',
        'path': '',
        'has_parent': False,
    }


def get_file_list(filepath):
    if os.path.exists(filepath) is False or os.path.isdir(filepath) is False:
        return []
    files = []
    for filename in os.listdir(filepath):
        filetype = get_filetype(filepath, filename)
        files.append({
            'filename': filename,
            'type': filetype,
            'cls': get_css_class(filetype),
        })
    return files


def get_filetype(filepath, filename):
    extension = os.path.splitext(filename)[1]
    extensions = {
        'movie': ['.mov', '.avi', '.mp4'],
        'audio': ['.mp3', '.wav'],
        'picture': ['.gif', '.jpeg', '.jpg', '.tiff', '.png'],
        'archive': ['.zip', '.tar.bz2', '.tar.gz', '.gz'],
        'code': ['.py', '.pp', '.yaml', '.sh', '.rb'],
        'pdf': ['.pdf'],
        'excel': ['.xls', '.xlsx'],
        'word': ['.doc', '.docx'],
        'text': ['.log', '.txt'],
    }
    filetype = 'other'
    for type, exts in extensions.items():
        if extension in exts:
            filetype = type
    if os.path.isdir(os.path.join(filepath, filename)):
        filetype = 'folder'
    return filetype


def get_css_class(filetype):
    types = {
        'movie': 'file-video-o',
        'audio': 'file-audio-o',
        'picture': 'file-image-o',
        'archive': 'file-archive-o',
        'code': 'file-code-o',
        'pdf': 'file-pdf-o',
        'excel': 'file-excel-o',
        'word': 'file-word-o',
        'text': 'file-text-o',
        'folder': 'folder-o',
        'other': 'file-o',
    }
    return types.get(filetype)


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
    basepath = request.registry.settings.get('fileexplorer.path')
    filepath = os.path.join(basepath, *request.matchdict.get('path'))
    if os.path.exists(filepath) is False:
        raise HTTPNotFound
    request_path = request.matchdict.get('path')
    path = ''
    has_parent = False
    if len(request_path) > 0:
        path = '{0}/'.format(os.path.join(*request_path))
        has_parent = True
    parent_path = ''
    if len(request_path) > 1:
        parent_path = '{0}/'.format(os.path.join(*request_path[:-1]))
    return {
        'files': get_file_list(filepath),
        'path': path,
        'parent': parent_path,
        'has_parent': has_parent,
    }
