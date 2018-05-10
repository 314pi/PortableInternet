#!/bin/python
# -*- coding: iso-8859-1 -*-

"""
GenericDispatch.py (WX)

David Janes
Algorithmics
2004.05.08

Make sure methods are called in the correct (wx) thread.
This is _really_ useful in multihreaded WX applications
"""

#
# Copyright (C) 2004 David P. Janes
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later
# version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA
#
# CREDIT TO "David P. Janes" AND "BlogMatrix" WOULD BE APPRECIATED
# Donations gratefully accepted at "http://jaeger.blogmatrix.com/donate/".
#


import sys

from wxPython.wx import *
from wxPython.lib import newevent

DispatchEvent, EVT_DISPATCH = newevent.NewEvent()

class GenericDispatchMixin:
	def __init__(self):
		EVT_DISPATCH(self, self.OnDispatchEvent)

	def OnDispatchEvent(self, event):
		event.method(*event.arguments)

	def ThreadSafeDispatch(self, method, *arguments):
		wxPostEvent(self, DispatchEvent(method = method, arguments = arguments))

