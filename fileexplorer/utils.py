# -*- coding: utf-8 -*-
"""
fileexplorer
------------

Created by mpeeters
:copyright: (c) 2016 by NetExpe SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import os


def get_path(request):
    """Return the path extracted from the request"""
    basepath = request.registry.settings.get('fileexplorer.path')
    return os.path.join(basepath, *request.matchdict.get('path') or [])
