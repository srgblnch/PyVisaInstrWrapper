#=============================================================================
#
# file :        remoteCommandsRSG.py
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

class RSGInstructionSet(remoteCommands.InstructionSet):
    def __init__(self,debug=False):
        remoteCommands.InstructionSet.__init__(self)
        self._debug = debug
        self.trace("RSGInstructionSet.__init__()")

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
                return {'frequency':          self.frequency_read,
                        'frequencyRangeLow':  self.frequencyRangeLow_read,
                        'frequencyRangeHigh': self.frequencyRangeHigh_read,
                        'powerRangeLow':      self.powerRangeLow_read,
                        'powerRangeHigh':     self.powerRangeHigh_read,
                        'phaseContinuousFrequencyActive':self.phaseContinuousFrequencyActive_read,
                        'phaseContinuousFrequencyNarrow':self.phaseContinuousFrequencyNarrow_read,
                        'powerLevel':         self.powerLevel_read,
                        'rf':                 self.rf_read,
                        'impedancy':          self.impedancy_read,
                        'oscRefSrc':          self.oscRefSrc_read,
                        'oscExtFreq':         self.oscExtFreq_read,
                        'oscExtRf':           self.oscExtRf_read,
                        'oscExtNarrow':       self.oscExtNarrow_read,
                        'errors':             self.errors_read,
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
                return {'frequency':          self.frequency_write,
                        #'frequencyRangeLow':  self.frequencyRangeLow_write,
                        #'frequencyRangeHigh': self.frequencyRangeHigh_write,
                        #'powerRangeLow':      self.powerRangeLow_write,
                        #'powerRangeHigh':     self.powerRangeHigh_write,
                        'phaseContinuousFrequencyActive':self.phaseContinuousFrequencyActive_write,
                        'phaseContinuousFrequencyNarrow':self.phaseContinuousFrequencyNarrow_write,
                        'powerLevel':         self.powerLevel_write,
                        'rf':                 self.rf_write,
                        'oscRefSrc':          self.oscRefSrc_write,
                        'oscExtFreq':         self.oscExtFreq_write,
                        'oscExtRf':           self.oscExtRf_write,
                        'oscExtNarrow':       self.oscExtNarrow_write,
                        }[key](value)
        except Exception,e:
            msg = "Exeption on send of key %s: %s"%(key,e)
            self.trace(msg)
            raise e

class RohdeSchwarz(RSGInstructionSet):
    def __init__(self,debug=False):
        RSGInstructionSet.__init__(self, debug)
        self.trace("Rohde&Schwarz.__init__()")

    def frequency_read(self):
        return ":FREQ?"
    def frequency_write(self,value):
        return ":FREQ %s"%str(value)
    
    def frequencyRangeLow_read(self):
        return ":FREQ:PHAS:CONT:LOW?"
    #def frequencyRangeLow_write(self,value):
    #    return ":FREQ:PHAS:CONT:LOW %s"%(str(value))
    
    def frequencyRangeHigh_read(self):
        return ":FREQ:PHAS:CONT:HIGH?"
    #def frequencyRangeHigh_write(self,value):
    #    return ":FREQ:PHAS:CONT:HIGH%s"%(str(value))
    
    def powerRangeLow_read(self):
        return ":OUTP:AFIX:RANG:LOW?"
    #def powerRangeLow_write(self,value):
    #    return ":OUTP:AFIX:RANG:LOW %s"%(str(value))
    
    def powerRangeHigh_read(self):
        return ":OUTP:AFIX:RANG:UPP?"
    #def powerRangeHigh_write(self,value):
    #    return ":OUTP:AFIX:RANG:UPP %s"%(str(value))

    def phaseContinuousFrequencyActive_read(self):
        return ":FREQ:PHAS:CONT:STAT?"
    def phaseContinuousFrequencyActive_write(self,value):
        return ":FREQ:PHAS:CONT:STAT %s"%("ON" if bool(value) else "OFF")
    
    def phaseContinuousFrequencyNarrow_read(self):
        return ":FREQ:PHAS:CONT:MODE?"
    def phaseContinuousFrequencyNarrow_write(self,value):
        return ":FREQ:PHAS:CONT:MODE %s"%("NARROW" if bool(value) else "WIDE")

    def powerLevel_read(self):
        return ":POW?"
    def powerLevel_write(self,value):
        return ":POW %s"%str(value)

    def rf_read(self):
        return ":OUTP:STAT?"
    def rf_write(self,value):
        return ":OUTP:STAT %s"%("ON" if bool(value) else "OFF")
    
    def impedancy_read(self):
        return ":OUTP:IMP?"
    
    def oscRefSrc_read(self):
        return ":ROSCillator:SOURce?"
    def oscRefSrc_write(self,value):
        return ":ROSCillator:SOURce %s"%("EXT" if bool(value) else "INT")
    
    def oscExtFreq_read(self):
        return ":ROSCillator:EXTernal:FREQuency?"
    def oscExtFreq_write(self,value):
        return ":ROSCillator:EXTernal:FREQuency %s"%(str(value))

    def oscExtRf_read(self):
        return ":ROSCillator:EXTernal:RFOFf:STATe?"
    def oscExtRf_write(self,value):
        return ":ROSCillator:EXTernal:RFOFf:STATe %s"%("ON" if bool(value) else "OFF")
    
    def oscExtNarrow_read(self):
        return ":ROSCillator:EXTernal:SBANdwidth?"
    def oscExtNarrow_write(self,value):
        return ":ROSCillator:EXTernal:SBANdwidth %s"%("NARROW" if bool(value) else "WIDE")
    
    def errors_read(self):
        return ":SYST:SERROR?"
