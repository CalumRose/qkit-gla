# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:15:20 2023

@author: admin
"""

import qkit
from qkit.core.instrument_base import Instrument

from qkit import visa 

import logging

class ThorLabs_PM100D(Instrument):
    '''
    This is the driver for the ThorLabs_PM100D OPtical Power Meter
    Usage:
    Initialize with
    <name> = qkit.instruments.create('<name>', 'ThorLabs_PM100D', address='<IP address>', reset=<bool>)
    '''

    def __init__(self, name, address, reset=False):
        '''
        Initializes the power meter, and communicates with the wrapper.
        
        Input:
            name (string)    : name of the instrument
            address (string) : IP address
            reset (bool)     : resets to default values, default=False
        '''
        # Start VISA communication
        logging.info(__name__ + ': Initializing instrument ThorLabs PM100D')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.read_termination="\n"
        self._visainstrument.timeout = 5000

        
        def reset(self):
            self._visainstrument.write('*RST')
        
        def do_get_wavelength(self):
            return self._visainstrument.query('SENS:CORR:WAV?')
        
        def do_set_wavelength(self,wavelength):
            self._visainstrument.write('SENS:CORR:WAV' + str(wavelength))

            
        def do_measure_power(self):
            return self._visainstrument.query('MEAS:POW?')
            
