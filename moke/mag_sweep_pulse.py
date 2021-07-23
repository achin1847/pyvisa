
import visa
import matplotlib.pyplot as plt
import numpy as np
import time
usleep = lambda x: time.sleep(x/1000000.0)

# -----------------------------------------------------------
# Function
# -----------------------------------------------------------
def set_pulse_timing(hold_time, meas_delay, period, pulse_width):
    """
    set pulse timing for ADCMT

    Parameters
    ----------
    hold_time (ms)  : Th
    meas_delay (ms) : Td
    period (ms)     : Tp
    pulse_width (ms): Tw

    Constants for timing
    -----
    Tds(source delay time) + 300us < Tp
    Td + 300us < Tp
    Tds <= Td
    Tds + Tw + 300us < Tp
    600ms <= Tp
    """
    ADCMT.write('SP'+str(hold_time)+','+str(meas_delay)+','+str(period)+','+str(pulse_width))
# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ADCMT = rm.open_resource('GPIB0::27::INSTR') # out-of-plane
print(ADCMT.query('*IDN?'))

ADCMT.write('*RST;*CLS')
# -----------------------------------------------------------
# Mode Settings:
# ----------------------------------------------------------
ADCMT.write('OH1') # header on
ADCMT.write('M1')  # trigger mode hold
ADCMT.write('IF')  # current output
ADCMT.write('F1')  # voltage measurement
ADCMT.write('MD1')  # pulse gen
# -----------------------------------------------------------
# Constants
# -----------------------------------------------------------
mag_pulse_curr = 0.1
HOLD_TIME = 3
MEAS_DELAY = 1
PERIOD = 1300
PULSE_WIDTH = 500
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
ADCMT.write('LMV3')  # limit 3V
ADCMT.write('DBI0')  # pulse base 0A
set_pulse_timing(HOLD_TIME, MEAS_DELAY, PERIOD, PULSE_WIDTH)
for loop in range(100):
    ADCMT.write('SOI%f' % 0.2)
    ADCMT.write('OPR') # output on
    usleep(100000)
    ADCMT.write('SOI%f' % -0.2)
    ADCMT.write('OPR') # output on
    usleep(100000)
ADCMT.timeout = 2000  # Acquisition timeout in milliseconds - set it higher than the acquisition time
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition

ADCMT.write('SBY')  # output off
ADCMT.query('*OPC?')

ADCMT.close()
