#!/usr/bin/env python2.5

#=============================================================================
#
# file :        threadVisa.py
#
# description : Methods to maintain the connection alive to a visa device.
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
import threading
import array

import traceback

def cutlongstrings(string,length):
    if len(string)<length: return string
    else: return "%s...(+%s)"%(string[:length].__repr__(),len(string)-length)
    #return len(string)<length and string or "%s...(+%s)"%(string[:length],len(string)-length)


def flatten(x):
    """from: http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
    flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def group(lst, n):
    """from: http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/
    group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
    
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.
    
    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    
    this have problems if the lenght of the list is not divisible by n, 
    it forgets the incomplete last one.
    """
    #return zip(*[lst[i::n] for i in range(n)])
    if n <= 0 or len(lst) < n: return [tuple(lst)]
    res = zip(*[lst[i::n] for i in range(n)])
    tail = tuple(lst[(len(lst)/n)*n:])
    res.append(tail)
    return res


class ThreadVisa:#(PyTango.Device_4Impl):
    """ Threading area to reconnect to the visa device without kill/start this device.
        @todo  Split the threading on a class apart
    """
    
#    def __init__(self,cl, name):
#        PyTango.Device_4Impl.__init__(self,cl,name)

    def startThread(self,time = 1):
        self.setReconnectTimeWait(time)
        if hasattr(self,'__thread') and self.__thread and self.__thread.isAlive():
            self.warn_stream("In %s::startThread(): Trying to start threading when is already started."%self.get_name())
            return
        self.info_stream("In %s::startThread(): Starting threading."%self.get_name())
        self.__threaded = True
        self.__joinerEvent = threading.Event()#to communicate between threads
        self.__joinerEvent.clear()
        self.__connectionEvent = threading.Event()#set when communications fails
        self.__connectionEvent.clear()
        self.__thread = threading.Thread(target=self.connect)
        self.__thread.setDaemon(True)
        self.__thread.start()

    def stopThread(self):
        self.info_stream("In %s::stopThread(): Stoping threading."%self.get_name())
        #TODO: about the __connectionEvent ???
        if hasattr(self,'__joinerEvent'):
            self.__joinerEvent.set()
        if hasattr(self,'__thread'):
            self.__thread.join()

    def connect(self):
        """ Method to be looped by the thread responsible for the (re)connection.
            
            @todo this method need a severe refactoring.
        """

        repeatMsg = ""
        repeatMsgCnt = 0
        auxmsg = ""

        self.__visaScope = None
        self.__visaState = PyTango.DevState.UNKNOWN

        while not self.__joinerEvent.isSet():
            try:
                #1: connect
                self.__visaScope = PyTango.DeviceProxy(self.PyVisaDS)
                #2: mirror the state
                self.__visaState = self.__visaScope.state()
                #3: set the status related with the visa device
                self.set_state(self.__visaState)
                #4: configure the connection
                if self.__visaState in [PyTango.DevState.ON]:
                    self.link2dict()
                #5: passive sleep until a connection requires the action of this thread
                self.__connectionEvent.wait()
                self.__connectionEvent.clear()
            except Exception,e:
                self.set_state(PyTango.DevState.FAULT)
                msg = "In %s::connect():(re)connection thread exception: %s"%(self.get_name(),e)
                if repeatMsg == msg:
                    repeatMsgCnt += 1
                else:
                    if not repeatMsgCnt == 0:
                        self.warn_stream("In %s::connect():last message repeated %d times"%(self.get_name(),repeatMsgCnt))
                    self.exceptionStatus("communication exception: %s"%e[0].desc)
                    self.error_stream(msg)
                    repeatMsg = msg
                    repeatMsgCnt = 0
                self.__connectionEvent.wait(self.getReconnectTimeWait())
                self.debug_stream("In %s::connect() connectionEvent = %s"%(self.get_name(),self.__connectionEvent.isSet()))
                self.__connectionEvent.clear()
        #out the loop means the thread has to finish and join the main one.
        self.info_stream("In %s::connect():thread exiting"%self.get_name())

    def fixVisaAttrs(self):#maybe more than timeout in the future
        try:
            timeout = self.__visaScope.read_attribute('Timeout')
            if not timeout.w_value == timeout.value and not timeout.w_value == 0:
                self.debug_stream("In %s::fixVisaAttrs() timeout w_value=%f,value%f"%(self.get_name(),timeout.w_value,timeout.value))
                self.__visaScope.write_attribute('timeout',timeout.w_value)
        except Exception,e:
            print("In %s::fixVisaAttrs() Exception: %s"%(self.get_name(),e))

    def force_reconnect(self):
        self.warn_stream("In %s::force_reconnect():wake up the connection thread to ask again the visa device"%self.get_name())
        self.__connectionEvent.set()

    def getReconnectTimeWait(self):
        return self.__reconnectTimeWait

    def setReconnectTimeWait(self,time):
        self.__reconnectTimeWait = time
    #done threading area

    #communications with visa area
    def ask(self,visacommand):
        """A combination of write(message) and read()"""
        self.debug_stream("In %s::ask() query=%s"%(self.get_name(),visacommand))
        try:
            if not self.__visaScope == None and self.__visaScope.state() in [PyTango.DevState.ON]:
                answer = array.array('B',self.__visaScope.Ask(array.array('B',visacommand).tolist())).tostring()
                self.debug_stream("In %s::ask() answer= %s"%(self.get_name(),cutlongstrings(answer,self.logger_maxlen)))
                return answer
            else:
                return ""
        except Exception,e:
            traceback.print_exc()
            self.debug_stream("In %s::ask() Exception= %s"%(self.get_name(),e))
            self.set_state(PyTango.DevState.FAULT)
            self.error_stream("In %s::ask() Device goes to fault"%(self.get_name()))
            self.exceptionStatus(e)
            self.__visaScope = None
            self.__connectionEvent.set()
            raise Exception,e

    def ask_for_values(self,visacommand):
        """A combination of write(message) and read()"""
        self.debug_stream("In %s::ask_for_values() query= %s"%(self.get_name(),visacommand))
        try:
            if not self.__visaScope == None and self.__visaScope.state() in [PyTango.DevState.ON]:
                answer = self.__visaScope.AskValues(array.array('B',visacommand).tolist())
        except Exception,e:
            self.debug_stream("In %s::ask_for_values() Exception= %s"%(self.get_name(),e))
            self.set_state(PyTango.DevState.FAULT)
            self.error_stream("In %s::ask_for_values() Device goes to fault"%(self.get_name()))
            self.exceptionStatus(e)
            self.__visaScope = None
            self.__connectionEvent.set()
            raise Exception,e
        else:
            self.debug_stream("In %s::ask_for_values() answer= \"%s\""%(self.get_name(),cutlongstrings(answer,self.logger_maxlen)))
            return answer

    def write(self,visacommand):
        """Write a string message to the device."""
        self.debug_stream("In %s::write() \"%s\""%(self.get_name(),visacommand))
        try:
            if not self.__visaScope == None and self.__visaScope.state() in [PyTango.DevState.ON]:
                self.__visaScope.Write(array.array('B',visacommand).tolist())
        except Exception,e:
            self.debug_stream("In %s::write() Exception=\"%s"%(self.get_name(),e))
            self.set_state(PyTango.DevState.FAULT)
            self.error_stream("In %s::write() Device goes to fault"%(self.get_name()))
            self.exceptionStatus(e)
            self.__visaScope = None
            self.__connectionEvent.set()
            raise Exception,e

    def read(self):
        """Read a string from the device."""
        self.debug_stream("In %s::read()"%self.get_name())
        if not self.__visaScope == None and self.__visaScope.state() in [PyTango.DevState.ON]:
            return array.array('B',self.__visaScope.read())
        else:
            return
    #done communications with visa area

    def getVisaDS_state(self):
        return self.__visaScope.state()

    def setVisaDS_reset(self):
        try:
            self.__visaScope.Reset()
        except Exception,e:
            self.error_stream("In %s::setVisaDS_reset() Exception! %s"%(self.get_name(),e))

    def setVisaDS_init(self):
        try:
            self.__visaScope.Init()
        except Exception,e:
            self.error_stream("In %s::setVisaDS_init() Exception! %s"%(self.get_name(),e))

    def exceptionStatus(self,argin=None):
        try:
            msg = "The device is in %s state."%(self.get_state())
            if not argin == None:
                msg += "\n"
                for i,element in enumerate(argin):
                    if type(element) == PyTango.DevError:
                        msg += str(element.desc)+"\n"
                    else:
                        msg += str(element)
        except Exception,e:
            msg += str(e)
        self.set_status(msg)
