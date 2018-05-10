# -*- coding: utf-8 -*-
# gpodder.net API Client
# Copyright (C) 2009-2013 Thomas Perl and the gPodder Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""gpodder.net API Client Library

This is mygpoclient, the gpodder.net API Client Library for Python.
"""

__author__ = 'Thomas Perl <thp@gpodder.org>'
__version__ = '1.8'
__website__ = 'http://gpodder.org/mygpoclient/'
__license__ = 'GNU General Public License v3 or later'

# Default settings for the API client (server root url and API version)
ROOT_URL = 'http://gpodder.net'
VERSION = 2
TOPLIST_DEFAULT = 50

# You can overwrite this value from your application if you want
user_agent = 'mygpoclient/%s (+%s)' % (__version__, __website__)

# Version checking
def require_version(minimum_required):
    """Require a minimum version of the library

    Returns True if the minimum library version constraint is
    satisfied, False otherwise. Use this to check for newer API
    methods and changes in the public API as described in NEWS.

    >>> require_version('1.0')
    True
    >>> require_version('1.2')
    True
    >>> require_version(__version__)
    True
    >>> require_version('99.99')
    False
    """
    this_version = [int(x) for x in __version__.split('.')]
    minimum_required = [int(x) for x in minimum_required.split('.')]
    return minimum_required <= this_version

