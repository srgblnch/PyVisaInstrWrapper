#=============================================================================
#
# file :        remoteCommandsRTS.py
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

import remoteCommands

class RTSInstructionSet(remoteCommands.InstructionSet):
    def __init__(self,debug=False):
        remoteCommands.InstructionSet.__init__(self)
        self._debug = debug
        self.trace("RTSInstructionSet.__init__()")

    def query(self,key,ch=None):
        """this method calls the corresponding method following a dictionary.
           The usage is only to read, because this is think to concatenate all
           reads in only one 'ask' to the scope. The writes will be executed one by one.
        """
        try:
            if not ch == None:
                return {'':    None,
                        }[key](ch)
            else:
                return {'lock':          self.lock_read,
                        'modes':         self.modes_read,
                        'mode':          self.mode_read,
                        'waveform':      self.waveform_read,
                        'spectrogram':   self.spectrogram_read,
                        }[key]()
        except Exception,e:
            msg = "Exeption on query of key %s: %s"%(key,e)
            self.trace(msg)

    def send(self,key,ch=None,value=None):
        """this method calls the corresponding method following a dictionary.
           The usage is to use a write method on the pyvisa
        """
        try:
            if not ch == None:
                return {'':    None,
                        }[key](ch,value)
            else:
                return {'lock':          self.lock_write,
                        'mode':          self.mode_write,
                        }[key](value)
        except Exception,e:
            msg = "Exeption on send of key %s: %s"%(key,e)
            self.trace(msg)


class Tektronix(RTSInstructionSet):
    def __init__(self,debug=False):
        RTSInstructionSet.__init__(self, debug)
        self.trace("Tektronics.__init__()")

    def lock_read(self):
        return ":SYSTem:KLOCk?"
    def lock_write(self,value):
        value = bool(value)
        return ":SYSTem:KLOCk %s"%("ON" if bool(value) else "OFF")

    def modes_read(self):
        return ":INSTrument:CATalog?"

    def mode_read(self):
        return ":INSTrument:SELect?"
    def mode_write(self,value):
        value = str(value)
        if not value in ["SARTIME","SASGRAM"]:
            raise Exception("Not yet supported mode!")
        return ":INSTrument:SELect %s"%value

    def waveform_read(self):
        return ":READ:SPECtrum?"

    def spectrogram_read(self):
        raise Exception("Not yet supported!")
        #return ":DISPlay:OVIew:FORMat SGRam"

