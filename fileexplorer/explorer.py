# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from pyramid.httpexceptions import HTTPNotFound

import os


class Folder(object):

    def __init__(self, request):
        self.request = request
        self.basepath = os.path.join(
            request.registry.settings.get('fileexplorer.path'),
            *self.request_path
        )
        self.elements = self._file_list()
        if os.path.exists(self.basepath) is False:
            raise HTTPNotFound

    def _file_list(self):
        if os.path.exists(self.basepath) is False or \
           os.path.isdir(self.basepath) is False:
            return []
        files = []
        for filename in os.listdir(self.basepath):
            files.append(Element(self.basepath, filename))
        return files

    @property
    def request_path(self):
        return self.request.matchdict.get('path', [])

    @property
    def has_parent(self):
        return len(self.request_path) > 0

    @property
    def path(self):
        if len(self.request_path) > 0:
            return '{0}/'.format(os.path.join(*self.request_path))
        return ''

    @property
    def parent_path(self):
        if len(self.request_path) > 1:
            return '{0}/'.format(os.path.join(*self.request_path[:-1]))
        return ''


class Element(object):
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

    type_icons = {
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

    def __init__(self, basepath, filename):
        self.basepath = basepath
        self.filename = filename

    @property
    def filetype(self):
        extension = os.path.splitext(self.filename)[1]
        _type = 'other'
        for type, exts in self.extensions.items():
            if extension in exts:
                _type = type
        if os.path.isdir(os.path.join(self.basepath, self.filename)):
            _type = 'folder'
        return _type

    @property
    def css_class(self):
        return self.type_icons.get(self.filetype)
