#!/usr/bin/env python2.5

#=============================================================================
#
# file :        PyVisainstrWrapper.py
#
# description : Python source for the VisaInstrument Super server. 
#
# project :     TANGO Device Server
#
# Author: sblanch (first developer)
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    Cells / Alba Synchrotron
#               Cerdanyola/Bellaterra
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

import PyTango

import sys

from PyScope import *
from PyAFGenerator import *
from PyRealTimeSpectrum import *
from PyRfSignalGenerator import *

#==================================================================
#
#    VisaInstrument class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        py = PyTango.Util(sys.argv)
        py.add_TgClass(ScopeClass,Scope,'Scope')
        py.add_TgClass(FunctionGeneratorClass,FunctionGenerator,'FunctionGenerator')
        py.add_TgClass(RealTimeSpectrumClass,RealTimeSpectrum,'RealTimeSpectrum')
        py.add_TgClass(RfSignalGeneratorClass,RfSignalGenerator,'RfSignalGenerator')

        U = PyTango.Util.instance()
        U.server_init()
        print "Ready to accept request"
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e
