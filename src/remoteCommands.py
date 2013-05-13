#=============================================================================
#
# file :        remoteCommands.py
#
# description :
#
# project :    
#
# $Author: sblanch $
#
# $Revision:  $
#
# copyleft :    Cells / Alba Synchrotron
#               Bellaterra
#               Spain
#
#=============================================================================
#
# This file is part of Tango-ds project.
#
# Tango-ds project is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Tango-ds project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#=============================================================================

class InstructionSet:
    """ Really abstract super class for the visa sets of instructions."""
    def __init__(self):
        pass
    def identify(self):
        return "*IDN?"
    def lock_write(self,value):
        raise Exception("Not generic") #!!
    def trace(self,text):
        if self._debug:
            print str(text)

