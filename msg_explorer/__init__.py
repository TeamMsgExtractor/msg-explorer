#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Date Format: YYYY-MM-DD

"""
msg-explorer:
    A GUI program to explore the contents of an MSG file using extract-msg.

https://github.com/TeamMsgExtractor/msg-explorer
"""

# --- LICENSE.txt -----------------------------------------------------------------
#
#    Copyright 2022 Destiny Peterson
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Destiny Peterson'
__date__ = '2022-06-06'
__version__ = '1.1.0'

# When this module is imported, we should try to compile the forms. They only
# compile when they are outdated.
from ._recompile import compile as _compile


_compile()
