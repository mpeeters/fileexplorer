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
        files.sort(key=lambda x: x.sort)
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

    @property
    def path_list(self):
        paths = []
        for idx, value in enumerate(self.request_path):
            paths.append((
                value,
                os.path.join(*self.request_path[:idx + 1]),
            ))
        return paths


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
        self.filetype = self._get_filetype()

    def _get_filetype(self):
        extension = os.path.splitext(self.filename)[1]
        _type = 'other'
        for type, exts in self.extensions.items():
            if extension in exts:
                _type = type
        if os.path.isdir(self.filepath):
            _type = 'folder'
        return _type

    @property
    def filepath(self):
        return os.path.join(self.basepath, self.filename)

    @property
    def filesize(self):
        if self.filetype == 'folder':
            return ''
        size = os.path.getsize(self.filepath)
        unit = 'B'
        factor = 1
        sizes = {
            1024. * 1024 * 1024 * 1024: 'TB',
            1024. * 1024 * 1024: 'GB',
            1024. * 1024: 'MB',
            1024.: 'KB',
        }
        for s, u in sizes.items():
            if size > s:
                unit = u
                factor = s
                break
        size = round(size / factor, 1)
        if unit in ('B', 'KB'):
            size = int(size)
        return '{0} {1}'.format(size, unit)

    @property
    def css_class(self):
        return self.type_icons.get(self.filetype)

    @property
    def sort(self):
        if self.filetype == 'folder':
            return '!!!_{0}'.format(self.filename)
        return self.filename
