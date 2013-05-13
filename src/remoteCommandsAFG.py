#=============================================================================
#
# file :        remoteCommandsAFG.py
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

from cStringIO import StringIO #For goodly fast str concat

class AFGInstructionSet(remoteCommands.InstructionSet):
    def __init__(self,debug=False):
        remoteCommands.InstructionSet.__init__(self)
        self._debug = debug
        self.trace("AFGInstructionSet.__init__()")

    def query(self,key,ch=None,mode=None):
        """this method calls the corresponding method following a dictionary.
           The usage is only to read, because this is think to concatenate all
           reads in only one 'ask' to the scope. The writes will be executed one by one.
        """
        try:
            if not ch == None:
                if not mode == None:
                    return {'modulatedShape':     self.modulatedShape_read,
                            'modulatedFrequency': self.modulatedFrequency_read,
                            'modulatedDepth':     self.modulatedDepth_read,
                            'modulatedDeviation': self.modulatedDeviation_read,
                            'modulatedRate':      self.modulatedRate_read,
                            }[key](ch,mode)
                return {'channelDisplay':    self.channelDisplay_read,
                        'function':          self.function_read,
                        'frequency':         self.frequency_read,
                        'amplitude':         self.amplitude_read,
                        'offset':            self.offset_read,
                        'high':              self.high_read,
                        'low':               self.low_read,
                        'phase':             self.phase_read,
                        'rampSymmetry':      self.rampSymmetry_read,
                        'pulseWidth':        self.pulseWidth_read,
                        'pulseLead':         self.pulseLead_read,
                        'pulseTrail':        self.pulseTrail_read,
                        'runMode':           self.runMode_read,
                        'sweepTime':         self.sweepTime_read,
                        'sweepHtime':        self.sweepHtime_read,
                        'sweepRtime':        self.sweepRtime_read,
                        'sweepSpacing':      self.sweepSpacing_read,
                        'sweepMode':         self.sweepMode_read,
                        'sweepFreqStart':    self.sweepFreqStart_read,
                        'sweepFreqStop':     self.sweepFreqStop_read,
                        'sweepFreqSpan':     self.sweepFreqSpan_read,
                        'sweepFreqCenter':   self.sweepFreqCenter_read,
                        }[key](ch)
            else:
                return {'lock':              self.lock_read,
                        'click':             self.click_read,
                        'beeper':            self.beeper_read,
                        'error':             self.error_read,
                        }[key]()
        except Exception,e:
            msg = "Exeption on query of key %s: %s"%(key,e)
            self.trace(msg)
            raise Exception,e

    def send(self,key,ch=None,value=None,mode=None):
        """this method calls the corresponding method following a dictionary.
           The usage is to use a write method on the pyvisa
        """
        try:
            if not ch == None:
                if not mode == None:
                    return {'modulatedShape':     self.modulatedShape_write,
                            'modulatedFrequency': self.modulatedFrequency_write,
                            'modulatedDepth':     self.modulatedDepth_write,
                            'modulatedDeviation': self.modulatedDeviation_write,
                            'modulatedRate':      self.modulatedRate_write,
                            }[key](ch,mode,value)
                return {'channelDisplay':    self.channelDisplay_write,
                        'function':          self.function_write,
                        'frequency':         self.frequency_write,
                        'amplitude':         self.amplitude_write,
                        'offset':            self.offset_write,
                        'high':              self.high_write,
                        'low':               self.low_write,
                        'phase':             self.phase_write,
                        'rampSymmetry':      self.rampSymmetry_write,
                        'pulseWidth':        self.pulseWidth_write,
                        'pulseLead':         self.pulseLead_write,
                        'pulseTrail':        self.pulseTrail_write,
                        'runMode':           self.runMode_write,
                        'sweepTime':         self.sweepTime_write,
                        'sweepHtime':        self.sweepHtime_write,
                        'sweepRtime':        self.sweepRtime_write,
                        'sweepSpacing':      self.sweepSpacing_write,
                        'sweepMode':         self.sweepMode_write,
                        'sweepFreqStart':    self.sweepFreqStart_write,
                        'sweepFreqStop':     self.sweepFreqStop_write,
                        'sweepFreqSpan':     self.sweepFreqSpan_write,
                        'sweepFreqCenter':   self.sweepFreqCenter_write,
                        }[key](ch,value)
            else:
                return {'lock':              self.lock_write,
                        'click':             self.click_write,
                        'beeper':            self.beeper_write,
                        }[key](value)
        except Exception,e:
            msg = "Exeption on send of key %s: %s"%(key,e)
            self.trace(msg)
            raise Exception,e

class Tektronix(AFGInstructionSet):
    def __init__(self,debug=False):
        AFGInstructionSet.__init__(self, debug)
        self.trace("Tektronics.__init__()")

    def lock_read(self):
        return ":SYSTem:KLOCk:STATe"
    def lock_write(self,value):
        value = bool(value)
        return ":SYSTem:KLOCk:STATe %s"%("ON" if bool(value) else "OFF")

    def click_read(self):
        return ":SYSTem:KCLick:STATe"
    def click_write(self,value):
        return ":SYSTem:KCLick:STATe %s"%("ON" if bool(value) else "OFF")

    def beeper_read(self):
        return ":SYSTem:BEEPer:STATe"
    def beeper_write(self,value):
        return ":SYSTem:BEEPer:STATe %s"%("ON" if bool(value) else "OFF")

    def error_read(self):
        return ":SYSTem:ERRor:NEXT?"

    def channelDisplay_read(self,ch):
        return ":OUTPut%d:STATE"%ch
    def channelDisplay_write(self,ch,value):
        value = str(value).lower()
        if value in [on,off,'1','0']:
            return ":OUTPut%d:STATE"%ch
        raise Exception("Not valid value")

    def runMode_read(self,ch):
        """ This block is really different than the rest. The continuous
           runMode is when all the other possibles are not activated.
        """
        query = StringIO()
        #The order has to be this, the same from the ds dict
        query.write(self.runMode_modulation_am_get(ch))
        query.write(";"+self.runMode_modulation_fm_get(ch))
        query.write(";"+self.runMode_modulation_fsk_get(ch))
        query.write(";"+self.runMode_modulation_pm_get(ch))
        query.write(";"+self.runMode_sweep_get(ch))
        return query.getvalue()
        
    def runMode_write(self,ch,value):
        bar = ""
        print "runMode_write(%d,%d)"%(ch,value)
        if value in [0,1,2,4,8]:
            bar = ":source%d:frequency:mode CW;"%(ch)
            bar += {
               0:self.runMode_continuous_set,
               1:self.runMode_modulation_am_set,
               2:self.runMode_modulation_fm_set,
               4:self.runMode_modulation_fsk_set,
               8:self.runMode_modulation_pm_set,
               #16:self.runMode_sweep_set,
              }[value](ch,"1")
        elif value in [16]:
            bar = self.runMode_sweep_set(ch,"1")
        print "return %s"%bar
        return bar
    def runMode_continuous_set(self,ch,val=None):
        #val not used, but compatible with other set methods
        send = StringIO()
        #The order has to be this, the same from the ds dict
        send.write(self.runMode_modulation_am_set(ch,"0"))
        send.write(";"+self.runMode_modulation_fm_set(ch,"0"))
        send.write(";"+self.runMode_modulation_fsk_set(ch,"0"))
        send.write(";"+self.runMode_modulation_pm_set(ch,"0"))
        #send.write(";"+self.runMode_sweep_set(ch,"0"))
        return send.getvalue()
        
    def runMode_modulation_am_get(self,ch):
        return ":source%d:am:state?"%ch
    def runMode_modulation_am_set(self,ch,val):
        return ":source%d:am:state %s"%(ch,val)
    def runMode_modulation_fm_get(self,ch):
        return ":source%d:fm:state?"%ch
    def runMode_modulation_fm_set(self,ch,val):
        return ":source%d:fm:state %s"%(ch,val)
    def runMode_modulation_fsk_get(self,ch):
        return ":source%d:fsk:state?"%ch
    def runMode_modulation_fsk_set(self,ch,val):
        return ":source%d:fsk:state %s"%(ch,val)
    def runMode_modulation_pm_get(self,ch):
        return ":source%d:pm:state?"%ch
    def runMode_modulation_pm_set(self,ch,val):
        return ":source%d:pm:state %s"%(ch,val)

    def runMode_sweep_get(self,ch):
        return ":source%d:frequency:mode?"%ch
    def runMode_sweep_set(self,ch,val):
        if val == "0": return ""
        elif val == "1": return ":source%d:frequency:mode SWE"%(ch)

    def function_read(self,ch):
        return ":SOURce%d:FUNCtion:SHAPe"%ch
    def function_write(self,ch,value):
        return ":SOURce%d:FUNCtion:SHAPe %s"%(ch,value)

    def modulatedShape_read(self,ch,mode):
        return ":SOURce%d:%s:INTernal:FUNCtion"%(ch,mode)
    def modulatedShape_write(self,ch,mode,value):
        return ":SOURce%d:%s:INTernal:FUNCtion %s"%(ch,mode,value)

    def modulatedFrequency_read(self,ch,mode):
        if mode in ["am","fm","pm"]: return ":SOURce%d:%s:INTernal:FREQuency"%(ch,mode)
        elif mode in ["fsk"]: return ":SOURce%d:%s:FREQuency"%(ch,mode)
        else: raise Exception("Not supported")
    def modulatedFrequency_write(self,ch,mode,value):
        if mode in ["am","fm","pm"]: return ":SOURce%d:%s:INTernal:FREQuency %s"%(ch,mode,value)
        elif mode in ["fsk"]: return ":SOURce%d:%s:FREQuency %s"%(ch,mode,value)
        else: raise Exception("Not supported")

    def modulatedDepth_read(self,ch,mode):
        if mode in ["am"]: return ":SOURce%d:%s:DEPTh"%(ch,mode)
        else: raise Exception("Not supported")
    def modulatedDepth_write(self,ch,mode,value):
        if mode in ["am"]: return ":SOURce%d:%s:DEPTh %s"%(ch,mode,value)
        else: raise Exception("Not supported")

    def modulatedDeviation_read(self,ch,mode):
        if mode in ["fm","pm"]: return ":SOURce%d:%s:DEViation"%(ch,mode)
        else: raise Exception("Not supported")
    def modulatedDeviation_write(self,ch,mode,value):
        if mode in ["fm","pm"]: return ":SOURce%d:%s:DEViation %s"%(ch,mode,value)
        else: raise Exception("Not supported")

    def modulatedRate_read(self,ch,mode):
        if mode in ["fsk"]: return ":SOURce%d:%s:INTernal:RATE"%(ch,mode)
        else: raise Exception("Not supported")
    def modulatedRate_write(self,ch,mode,value):
        if mode in ["fsk"]: return ":SOURce%d:%s:INTernal:RATE %s"%(ch,mode,value)
        else: raise Exception("Not supported")

    def frequency_read(self,ch):
        return ":SOURce%d:FREQuency"%ch
    def frequency_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:FREQuency %s"%(ch,value)

    def amplitude_read(self,ch):
        return ":SOURce%d:VOLTage:AMPLitude"%ch
    def amplitude_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:VOLTage:AMPLitude %s"%(ch,value)

    def offset_read(self,ch):
        return ":SOURce%d:VOLTage:OFFSet"%ch
    def offset_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:VOLTage:OFFSet %s"%(ch,value)

    def high_read(self,ch):
        return ":SOURce%d:VOLTage:HIGH"%ch
    def high_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:VOLTage:HIGH %s"%(ch,value)

    def low_read(self,ch):
        return ":SOURce%d:VOLTage:LOW"%ch
    def low_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:VOLTage:LOW %s"%(ch,value)

    def phase_read(self,ch):
        return ":SOURce%d:PHASe"%ch
    def phase_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:PHASe %s"%(ch,value)

    def rampSymmetry_read(self,ch):
        return ":SOURce%d:FUNCtion:RAMP:SYMMetry"%ch
    def rampSymmetry_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:FUNCtion:RAMP:SYMMetry %s"%(ch,value)

    def pulseWidth_read(self,ch):
        return ":SOURce%d:PULSe:WIDTh"%ch
    def pulseWidth_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:PULSe:WIDTh %s"%(ch,value)

    def pulseLead_read(self,ch):
        return ":SOURce%d:PULSe:TRANsition:LEADing"%ch
    def pulseLead_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:PULSe:TRANsition:LEADing %s"%(ch,value)

    def pulseTrail_read(self,ch):
        return ":SOURce%d:PULSe:TRANsition:TRAiling"%ch
    def pulseTrail_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":SOURce%d:PULSe:TRANsition:TRAiling %s"%(ch,value)

    def sweepTime_read(self,ch):
        return ":source%d:sweep:time"%ch
    def sweepTime_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:sweep:time %s"%(ch,value)

    def sweepHtime_read(self,ch):
        return ":source%d:sweep:htime"%ch
    def sweepHtime_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:sweep:htime %s"%(ch,value)

    def sweepRtime_read(self,ch):
        return ":source%d:sweep:rtime"%ch
    def sweepRtime_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:sweep:rtime %s"%(ch,value)

    def sweepSpacing_read(self,ch):
        return ":source%d:sweep:spacing"%ch
    def sweepSpacing_write(self,ch,value):
        value = str(value).lower()
        if value in ['lin','linear','log','logarithmic']:
            return ":source%d:sweep:spacing %s"%(ch,value)
        raise Exception("Not valid value")

    def sweepMode_read(self,ch):
        return ":source%d:sweep:mode"%ch
    def sweepMode_write(self,ch,value):
        value = str(value).lower()
        if value in ['auto','man']:
            return ":source%d:sweep:mode %s"%(ch,value)
        raise Exception("Not valid value")

    def sweepFreqStart_read(self,ch):
        return ":source%d:frequency:start"%(ch)
    def sweepFreqStart_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:frequency:start %s"%(ch,value)

    def sweepFreqStop_read(self,ch):
        return ":source%d:frequency:stop"%(ch)
    def sweepFreqStop_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:frequency:stop %s"%(ch,value)

    def sweepFreqSpan_read(self,ch):
        return ":source%d:frequency:span"%(ch)
    def sweepFreqSpan_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:frequency:span %s"%(ch,value)

    def sweepFreqCenter_read(self,ch):
        return ":source%d:frequency:center"%(ch)
    def sweepFreqCenter_write(self,ch,value):
        try: value = float(value)
        except: raise Exception("Not valid value")
        value = str(value).lower()
        return ":source%d:frequency:center %s"%(ch,value)