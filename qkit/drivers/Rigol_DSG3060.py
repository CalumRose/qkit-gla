# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 10:59:43 2023

@author: 2175469R
"""


from qkit.core.instrument_base import Instrument
from qkit import visa
import types
import logging
from time import sleep
import numpy


class Rigol_DSG3060(Instrument):
    '''
    This is the python driver for the Rigol DSG3060 Signal Generator
    It only provides very basic functionality

    Usage:
    Initialise with
    <name> = instruments.create('<name>', address='<GPIB address>', reset=<bool>)
    
    '''

    def __init__(self, name, address):
        '''
        Initializes the Rigol DSG3060, and communicates with the wrapper.

        Input:
            name (string)    : name of the instrument
            address (string) : GPIB address
        '''
        
        logging.info(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])

        self._address = address

        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.timeout=2000

        self._visainstrument.read_termination = '\n'
        self._visainstrument.write_termination = '\n'


        self.add_parameter('frequency',type = float,
            flags=Instrument.FLAG_GETSET,
            minval=9e3, maxval=6e9,
            units='Hz',tags=['sweep'])
        
        self.add_parameter('level', type = float,
            flags=Instrument.FLAG_GETSET,
            minval=-140, maxval=20,
            units='dBm',tags=['sweep'])
        
        self.add_parameter('state', type = bool,
            flags=Instrument.FLAG_GETSET)    

        
    # initialization related
    def get_all(self):
        self.get_frequency()
        self.get_power()
        self.get_status()
        
        
        
    def do_get_frequency(self):
        '''
        Get frequency of device

        Input:
            None

        Output:
            freq (float) : Frequency in Hz
            '''
        self._visainstrument.frequency = float(self.get(':SOUR:FREQ?'))
        return self._frequency
    
    def do_set_frequency(self,frequency):
        '''
        Set frequency of device

        Input:
            freq (float) : Frequency in Hz

        Output:
            None
        '''
        self._visainstrument.write(':SOUR:FREQ %i' % (int(frequency)))
        self._frequency = float(frequency)
        
    def do_get_level(self,level):
        '''
        Get power output of device

        Input:
            None

        Output:
            level (float) : Power in dBm
        '''
        self._level = float(self.get(':SOUR:LEV?'))
        
    def do_set_level(self,level):
        '''
        Set power output of device

        Input:
            level (float) : Power in dBm

        Output:
            None
        '''
        self.write('SOUR:LEV %i' % (int(level)))
        self._level = float(level)
        
    def do_get_state(self,state):
        '''
        Get power output of device

        Input:
            None

        Output:
            state (bool) : Output state
        '''
        self._level = float(self.get(':OUTP:STAT?'))
        
    def do_set_state(self,state):
        '''
        Set power output of device

        Input:
            state (bool) : Output state

        Output:
            None
        '''
        self.write(':OUTP:STAT %b' % (bool(state)))
        self._level = bool(state)
    
    #sending customized messages
    def write(self,msg):
      return self._visainstrument.write(msg)
    
    if visa.qkit_visa_version == 1:
        def ask(self,msg):
            return self._visainstrument.ask(msg)
    else:
        def ask(self, msg):
            return self._visainstrument.query(msg)
    
    
    
