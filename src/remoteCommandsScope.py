#=============================================================================
#
# file :        remoteCommandsScope.py
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

class ScopeInstructionSet(remoteCommands.InstructionSet):
    """ Superclass for the oscilloscopes visa Instructions sets."""
    def __init__(self,debug=False):
        remoteCommands.InstructionSet.__init__(self)
        self._debug = debug
        self.trace("ScopeInstructionSet.__init__()")
    def stop(self):
        return ":STOP"
    def run(self):
        return ":RUN"
    def operationComplete(self):
        return "*OPC?"
    def query(self,key,ch=None):
        """this method calls the corresponding method following a dictionary.
           The usage is only to read, because this is think to concatenate all
           reads in only one 'ask' to the scope. The writes will be executed one by one.
        """
        try:
            if not ch == None:
                return {'Amplitude':         self.amplitude_read,
                        'AmplitudeFn':       self.amplitudeFn_read,
                        'VPeakToPeak':       self.vpp_read,
                        'VPeakToPeakFn':     self.vppFn_read,
                        'VoltageMax':        self.voltageMax_read,
                        'VoltageMaxFn':        self.voltageMaxFn_read,
                        'VoltageMin':        self.voltageMin_read,
                        'VoltageMinFn':        self.voltageMinFn_read,
                        'VoltageUpper':      self.voltageUpper_read,
                        'VoltageLower':      self.voltageLower_read,
                        'Scale':             self.scale_read,
                        'Offset':            self.offset_read,
                        'RiseTime':          self.risetime_read,
                        'FallTime':          self.falltime_read,
                        'Period':            self.period_read,
                        'Frequency':         self.frequency_read,
                        'OverShoot':         self.overshoot_read,
                        'PreShoot':          self.preshoot_read,
                        'Impedance':         self.impedance_read,
                        'State':             self.channelDisplay_read,
                        'channelDisplay':    self.channelDisplay_read,
                        'Channel':           self.channel_read,
                        'StateFn':           self.functionDisplay_read,
                        'functionDisplay':   self.functionDisplay_read,
                        }[key](ch)
            else:
                return {'identify':          self.identify,
                        'OffsetH':           self.offsetH_read,
                        'ScaleH':            self.scaleH_read,
                        'Delay':             self.delay_read,
                        'CurrentSampleRate': self.currentSampleRate_read,
                        'Resolution':        self.resolution_read,
                        'TriggerType':       self.triggerType_read,
                        'TriggerLevel':      self.triggerLevel_read,
                        'TriggerSlope':      self.triggerSlope_read,
                        'TriggerSource':     self.triggerSource_read,
                        'sendvalid':         self.sendvalid_read,
                        'WaveformDataFormat':     self.WaveformDataFormat_read,
                        'ByteOrder':         self.byteOrder_read,
                        'WaveformOrigin':    self.waveformOrigin_read,
                        'WaveformIncr':      self.waveformIncr_read,
                        'AcquisitionMode':           self.acqmode_read,
                        'AcquisitionPoints':         self.acqpoints_read,
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
                return {'amplitude':         self.amplitude_write,
                        'scale':             self.scale_write,
                        'offset':            self.offset_write,
                        'impedance':         self.impedance_write,
                        'channelDisplay':    self.channelDisplay_write,
                        'functionDisplay':   self.functionDisplay_write,
                        'channel':           self.channel_write,
                        }[key](ch,value)
            else:
                return {'OffsetH':           self.offsetH_write,
                        'ScaleH':            self.scaleH_write,
                        'delay':             self.delay_write,
                        'currentSampleRate': self.currentSampleRate_write,
                        'resolution':        self.resolution_write,
                        'triggerType':       self.triggerType_write,
                        'triggerLevel':      self.triggerLevel_write,
                        'triggerSlope':      self.triggerSlope_write,
                        'triggerSource':     self.triggerSource_write,
                        'lock':              self.lock_write,
                        'sendvalid':         self.sendvalid_write,
                        'WaveformDataFormat':     self.WaveformDataFormat_write,
                        'ByteOrder':         self.byteOrder_write,
                        'AcquisitionMode':           self.acqmode_write,
                        'AcquisitionPoints':         self.acqpoints_write,
                        }[key](value)
        except Exception,e:
            msg = "Exeption on send of key %s: %s"%(key,e)
            self.trace(msg)

    def lock_write(self,value):
        raise Exception("Not generic") #!!
    def sendvalid_read(self):
        raise Exception("Not generic") #!!
    def sendvalid_write(self,value):
        raise Exception("Not generic") #!!

    ## The accepted queries to scopes
    def amplitude_read(self,ch):
        raise Exception("Not generic") #!!
    def amplitude_write(self,ch,value):
        raise Exception("Not generic") #!!
    def amplitudeFn_read(self,num):
        raise Exception("Not generic") #!!
    def vpp_read(self,ch):
        raise Exception("Not generic") #!!
    def vppFn_read(self,num):
        raise Exception("Not generic") #!!
    def voltageMax_read(self,ch):
        raise Exception("Not generic") #!!
    def voltageMin_read(self,ch):
        raise Exception("Not generic") #!!
    def voltageUpper_read(self,ch):
        raise Exception("Not generic") #!!
    def voltageLower_read(self,ch):
        raise Exception("Not generic") #!!
    def scale_read(self,ch):
        raise Exception("Not generic") #!!
    def scale_write(self,ch,value):
        raise Exception("Not generic") #!!
    def offset_read(self,ch):
        raise Exception("Not generic") #!!
    def offset_write(self,ch,value):
        raise Exception("Not generic") #!!
    def risetime_read(self,ch):
        raise Exception("Not generic") #!!
    def falltime_read(self,ch):
        raise Exception("Not generic") #!!
    def period_read(self,ch):
        raise Exception("Not generic") #!!
    def frequency_read(self,ch):
        raise Exception("Not generic") #!!
    def overshoot_read(self,ch):
        raise Exception("Not generic") #!!
    def preshoot_read(self,ch):
        raise Exception("Not generic") #!!
    def impedance_read(self,ch):
        raise Exception("Not generic") #!!
    def impedance_write(self,ch,value):
        raise Exception("Not generic") #!!
    def offsetH_read(self):
        raise Exception("Not generic") #!!
    def offsetH_write(self,value):
        raise Exception("Not generic") #!!
    def scaleH_read(self):
        raise Exception("Not generic") #!!
    def scaleH_write(self,value):
        raise Exception("Not generic") #!!
    def delay_read(self):#??r/w
        raise Exception("Not generic") #!!
    def delay_write(self):#??r/w
        raise Exception("Not generic") #!!
    def currentSampleRate_read(self):
        raise Exception("Not generic") #!!
    def currentSampleRate_write(self,value):
        raise Exception("Not generic") #!!
    def resolution_read(self):
        raise Exception("Not generic") #!!
    def resolution_write(self,value):
        raise Exception("Not generic") #!!
    def triggerType_read(self):
        raise Exception("Not generic") #!!
    def triggerType_write(self):
        raise Exception("Not generic") #!!
    def triggerLevel_read(self):
        raise Exception("Not generic") #!!
    def triggerLevel_write(self):
        raise Exception("Not generic") #!!
    def triggerSlope_read(self):
        raise Exception("Not generic") #!!
    def triggerSlope_write(self):
        raise Exception("Not generic") #!!
    def triggerSource_read(self):
        raise Exception("Not generic") #!!
    def triggerSource_write(self):
        raise Exception("Not generic") #!!
    def channelDisplay_read(self,ch):
        raise Exception("Not generic") #!!
    def channelDisplay_write(self,ch,value):
        raise Exception("Not generic") #!!
    def channel_read(self,ch):
        raise Exception("Not generic") #!!
    def WaveformDataFormat_read(self):
        raise Exception("Not generic") #!!
    def WaveformDataFormat_write(self,value):
        raise Exception("Not generic") #!!
    def channel_write(self,ch,value):
        raise Exception("Not generic") #!!
    def functionDisplay_read(self,ch):
        raise Exception("Not generic") #!!
    def functionDisplay_write(self,ch,value):
        raise Exception("Not generic") #!!
    def byteOrder_read(self):
        raise Exception("Not generic") #!!
    def byteOrder_write(self,value):
        raise Exception("Not generic") #!!
    def waveformOrigin_read(self):
        raise Exception("Not generic") #!!
    def waveformIncr_read(self):
        raise Exception("Not generic") #!!
    def acqmode_read(self):
        raise Exception("Not generic") #!!
    def acqmode_write(self,value):
        raise Exception("Not generic") #!!
    def acqpoints_read(self):
        raise Exception("Not generic") #!!
    def acqpoints_write(self,value):
        raise Exception("Not generic") #!!

class Agilent(ScopeInstructionSet):
    def __init__(self,debug=False):
        ScopeInstructionSet.__init__(self, debug)
        self.trace("Agilent.__init__()")
    def lock_write(self,value):
        value = bool(value)
        return ":SYSTem:LOCk %s"%("ON" if bool(value) else "OFF")
    def sendvalid_read(self):
        ":MEASure:SENDvalid?"
    def sendvalid_write(self,value):
        ":MEASure:SENDvalid %s"%("ON" if bool(value) else "OFF")
    def amplitude_read(self,ch):
        #return ":MEASure:VAMPlitude CHANnel%d;:MEASure:VAMPlitude?"%ch
        return ":MEASure:VAMPlitude? CHANnel%d"%ch
    def amplitudeFn_read(self,num):
        return ":MEASure:VAMPlitude? FUNCtion%d"%num
    def vpp_read(self,ch):
        return ":MEASure:VPP? CHANnel%d"%ch
    def vppFn_read(self,num):
        return ":MEASure:VPP? FUNCtion%d"%num
    def voltageMax_read(self,ch):
        return ":MEASure:VMAX? CHANnel%d"%ch
    def voltageMaxFn_read(self,ch):
        return ":MEASure:VMAX? FUNCtion%d"%ch
    def voltageMin_read(self,ch):
        return ":MEASure:VMIN? CHANnel%d"%ch
    def voltageMinFn_read(self,ch):
        return ":MEASure:VMIN? FUNCtion%d"%ch
    def voltageUpper_read(self,ch):
        return ":MEASure:VUPPer? CHANnel%d"%ch
    def voltageLower_read(self,ch):
        return ":MEASure:VLOWer? CHANnel%d"%ch
    def scale_read(self,ch):
        return ":CHANnel%d:SCALe?"%ch
    def scale_write(self,ch):
        value = str(value)
        return ":CHANnel%d:SCALe %s"%(ch,value)
    def offset_read(self,ch):
        return ":CHANnel%d:OFFSet?"%ch
    def offset_write(self,ch,value):
        value = str(value)
        return ":CHANnel%d:OFFSet %s"%(ch,value)
    def risetime_read(self,ch):
        return ":MEASure:RISEtime? CHANnel%d"%ch
    def falltime_read(self,ch):
        return ":MEASure:FALLtime? CHANnel%d"%ch
    def period_read(self,ch):
        return ":MEASure:PERiod? CHAN%d"%ch
    def frequency_read(self,ch):
        return ":MEASure:FFT:FREQuency? CHANnel%d"%ch
        #return ":MEASure:FREQuency? CHAN%d"%ch # the other seems fast responce
    def overshoot_read(self,ch):
        return ":MEASure:OVERshoot? CHANnel%d"%ch
    def preshoot_read(self,ch):
        return ":MEASure:PREShoot? CHANnel%d"%ch
    def impedance_read(self,ch):
        return ":CHANnel%d:INPut?"%ch
    def offsetH_read(self):
        return ":TIMebase:POS?"
    def offsetH_write(self,value):
        value = str(value)
        return ":TIMebase:POS %s"%str(value)
    def scaleH_read(self):
        return ":TIMebase:SCALe?"
    def scaleH_write(self,value):
        return ":TIMebase:SCALe %s"%str(value)
    def delay_read(self):
        raise Exception("Not available") #!!
    def currentSampleRate_read(self):
        return ":ACQuire:SRATe?"
    def currentSampleRate_write(self,value):
        value = str(value).lower()
        if value.isdigit() or (value in [auto,max]):
            return ":ACQuire:SRATe %s"%value #{ AUTO | MAX | <rate> }
        raise Exception("Not valid value")
    def resolution_read(self):
        raise Exception("Not available") #!!
    def resolution_write(self,value):
        raise Exception("Not available") #!!
    def triggerType_read(self):
        return ":TRIGger:MODE?"
    def triggerType_write(self,value):
        value = str(value).lower()
        if value in [edge,glit,glitch,adv,advanced]:
            if value in [glit,glitch,adv,advanced]:
                raise "Trigger type %s, not YET available"%value
            return ":TRIGger:MODE %s"%value #{ EDGE | GLITch | ADVanced }
        raise Exception("Not valid value")
    def triggerLevel_read(self):
        return ":TRIGger:LEVel?" 
    def triggerSlope_read(self):
        return ":TRIGger:EDGE:SLOPe?" #{ POSitive | NEGative | EITHer }
    def triggerSource_read(self):
        return ":TRIGger:EDGE:SOURce?" #{ CHANnel<N> | AUX | LINE }
    def channelDisplay_read(self,ch):
        return ":CHANnel%d:DISPlay?"%ch
    def channelDisplay_write(self,ch,value):
        try:
            print "ch %d Value %s"%(ch,value)
            value = str(value).lower()
            if value in ['on','off','1','0']:
                return ":CHANnel%d:DISPlay %s"%(ch,value)
            #raise Exception("Not valid value")
        except Exception,e:
            print "!"*20, "e"
    def channel_read(self,ch):
        """ Select the channel to transmit the curve, and send it as binary (fast)."""
        return ":WAVeform:SOURce CHANnel%d;:WAVeform:DATA?"%ch
    def WaveformDataFormat_read(self):
        return ":waveform:format?"
    def WaveformDataFormat_write(self,value):
        return ":waveform:format %s"%value
    def functionDisplay_read(self,num):
        return ":FUNCtion%d:DISPlay?"%num
    def functionDisplay_write(self,num,value):
        value = str(value).lower()
        if value in ['on','off','1','0']:
            return ":FUNCtion%d:DISPlay %s"%(num,value)
        raise Exception("Not valid value")
    def byteOrder_read(self):
        return ":WAVeform:BYTeorder?"
    def byteOrder_write(self,value):
        return ":WAVeform:BYTeorder %s"%value
    def waveformOrigin_read(self):
        return ":WAVeform:YORigin?"
    def waveformIncr_read(self):
        return ":WAVeform:YINCrement?"
    def acqmode_read(self):
        return ":ACQuire:MODE?"
    def acqmode_write(self,value):
        return ":ACQuire:MODE %s"%value
    def acqpoints_read(self):
        return ":ACQuire:POINts?"
    def acqpoints_write(self,value):
        return ":ACQuire:POINts %s"%value

class Tektronix(ScopeInstructionSet):
    def __init__(self,debug=False):
        ScopeInstructionSet.__init__(self, debug)
        self.trace("Tektronics.__init__()")
    def lock_write(self,value):
        value = bool(value)
        return ":LOCk %s"%("ON" if bool(value) else "OFF")
    def amplitude_read(self,ch):
        return ":MEASUrement:IMMed:TYPe AMPlitude;:MEASUrement:IMMed:SOURCE CH%d;MEASUrement:IMMed:VALue?"%ch
    def amplitudeFn_read(self,num):
        raise Exception("Not available") #!!
    def vpp_read(self,ch):
        raise Exception("Not available") #!!
    def vppFn_read(self,num):
        raise Exception("Not available") #!!
    def voltageMax_read(self,ch):
        raise Exception("Not available") #!!
    def voltageMin_read(self,ch):
        raise Exception("Not available") #!!
    def voltageUpper_read(self,ch):
        raise Exception("Not available") #!!
    def voltageLower_read(self,ch):
        raise Exception("Not available") #!!
    def scale_read(self,ch):
        return ":MEASUrement:IMMed:VALue?"
    def scale_read(self,ch,value):
        value = str(value)
        return ":MEASUrement:IMMed:VALue %s"%value
    def offset_read(self,ch):
        return ":ch%d:OFFSet?"%ch
    def offset_write(self,ch,value):
        value = str(value)
        return ":ch%d:OFFSet %s"%(ch,value)
    def risetime_read(self,ch):
        raise Exception("Not available") #!!
    def falltime_read(self,ch):
        raise Exception("Not available") #!!
    def period_read(self,ch):
        raise Exception("Not available") #!!
    def frequency_read(self,ch):
        raise Exception("Not available") #!!
    def overshoot_read(self,ch):
        raise Exception("Not available") #!!
    def preshoot_read(self,ch):
        raise Exception("Not available") #!!
    def impedance_read(self,ch):
        return ":ch%d:TERmination"%ch
    def offsetH_read(self):
        raise Exception("Not available") #!!
    def offsetH_write(self,value):
        raise Exception("Not available") #!!
    def scaleH_read(self):
        return ":HORizontal:SCAle?"
    def scaleH_write(self,value):
        value = str(value)
        return ":HORizontal:SCAle %s"%value
    def delay_read(self):
        raise Exception("Not available") #!!
    def currentSampleRate_read(self):
        return ":HORizontal:MAIn:SAMPLERate?"
    def currentSampleRate_write(self,value):
        value = str(value)
        return ":HORizontal:MAIn:SAMPLERate %s"%value
    def resolution_read(self):
        return ":hor:resolution?"
    def resolution_read(self,value):
        value = str(value)
        return ":hor:resolution %s"%value
    def triggerType_read(self):
        return ":TRIGger:A:TYPe?"
    def triggerType_write(self,value):
        value = str(value)
        return ":TRIGger:A:TYPe %s"%value
    def triggerLevel_read(self):
        return ":TRIGger:A:LEVel?"
    def triggerLevel_write(self,value):
        value = str(value)
        return ":TRIGger:A:LEVel %s"%value
    def triggerSlope_read(self):
        return ":TRIGger:A:EDGE:SLOpe?"
    def triggerSlope_write(self,value):
        value = str(value)
        return ":TRIGger:A:EDGE:SLOpe %s"%value
    def triggerSource_read(self):
        return ":TRIGger:A:EDGE:SOUrce?"
    def triggerSource_write(self,value):
        value = str(value)
        return ":TRIGger:A:EDGE:SOUrce %s"%value
    def channelDisplay_read(self,ch):
        return ":SELect:CH%d?"%ch
    def channelDisplay_write(self,ch,value):
        value = str(value)
        return ":SELect:CH%d %s"%(ch,value)
    def channel_read(self,ch):
        raise Exception("Not available") #!!
    def functionDisplay_read(self,num):
        raise Exception("Not available") #!!
    def functionDisplay_write(self,num,value):
        raise Exception("Not available") #!!
