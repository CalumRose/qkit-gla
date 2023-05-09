# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:44:48 2023

@author: admin
"""

import qkit
from qkit.core.instrument_base import Instrument

from qkit import visa 

import logging
import numpy
import time,sys

class Keithley_2200(Instrument):
    '''
    This is the driver for the Keithley 2200 Power Supply
    Usage:
    Initialize with
    <name> = qkit.instruments.create('<name>', 'Keithley_2200', address='<IP address>', reset=<bool>)
    '''

    def __init__(self, name, address, reset=False):
        '''
        Initializes the Keithley, and communicates with the wrapper.
        
        Input:
            name (string)    : name of the instrument
            address (string) : IP address
            reset (bool)     : resets to default values, default=False
        '''
        # Start VISA communication
        logging.info(__name__ + ': Initializing instrument Keithley 2220')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.read_termination="\n"
        self._visainstrument.timeout = 5000
        
        self.add_parameter('source_mode',
            flags=Instrument.FLAG_GETSET,
            type=str, units='')
            
        self.add_parameter('output',
            flags=Instrument.FLAG_GETSET ,
            units='', type=str)
        
        self.add_parameter('level', 
            flags=Instrument.FLAG_GETSET,
            type=float, units='')
        
    # functions
        def reset(self):     
            '''
            Resets instrument to default values

            Input:
                None
        
            Output:
                None
            '''
            logging.debug(__name__ + ' : Resetting instrument')
            self._visainstrument.write('*RST')

            
        def get_output(self):
            return self._visainstrument.query('OUTP?')
        
        def set_output(self,state):
            self._.write('OUTP'+str(state))
            
        def get_voltage_limit(self):
            return self._visainstrument.query('SOUR:VOLT:RANG?')
        
        def set_voltage_limit(self,limit):
            self._visainstrument.write('SOUR:VOLT:RANG'+str(limit))
            
        def get_voltage(self):
            return self._visainstrument.query('SOUR:VOLT:LEV?')
                    
        def set_voltage(self,voltage):
            self._visainstrument.write('SOUR:VOLT:LEV' + str(voltage))
            
        def get_current(self):
            return self._visainstrument.query('SOUR:CURR:LEV?')
                    
        def set_current(self,current):
            self._visainstrument.write('SOUR:CURR:LEV' + str(current))
            
        def measure_current(self):
            self._visainstrument.query('MEAS:CURR?')
            
        def measure_voltage(self):
            self._visainstrument.query('MEAS:VOLT?')
            
        
        
        
        
        
        
            
        