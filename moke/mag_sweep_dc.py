
import visa
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

# -----------------------------------------------------------
# Function
# -----------------------------------------------------------
def set_sweep(start, stop, step):
    """
    sweep configuration for ADCMT

    Parameters
    ----------
    start (A or V): start value of sweep
    stop (A or V) : stop value of sweep
    step (A or V) : step value of sweep
    """
    ADCMT.write('SN'+str(start)+','+str(stop)+','+str(step))

def set_pulse_timing(hold_time, meas_delay, period):
    """
    set pulse timing for ADCMT

    Parameters
    ----------
    hold_time (ms)  : Th
    meas_delay (ms) : Td
    period (ms)     : Tp
    """
    ADCMT.write('SP'+str(hold_time)+','+str(meas_delay)+','+str(period))
# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ADCMT = rm.open_resource('GPIB0::27::INSTR') # out-of-plane
print(ADCMT.query('*IDN?'))

ADCMT.write('*RST;*CLS')
ADCMT.write('*SRE8') # SRQ
ADCMT.write('S0') # SRQ
# ADCMT.write('*SRE8;DES8192;S0') # SRQ
# -----------------------------------------------------------
# Mode Settings:
# ----------------------------------------------------------
ADCMT.write('OH1') # header on
ADCMT.write('IF')  # current output
ADCMT.write('F1')  # voltage measurement
ADCMT.write('MD2')  # sweep gen mode
# -----------------------------------------------------------
# Constants
# -----------------------------------------------------------
START_CURR = -0.1
STOP_CURR = 0.1
STEP_CURR = 0.001

HOLD_TIME = 3
MEAS_DELAY = 4
PERIOD = 100
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
ADCMT.write('LMV3')  # limit 3V
ADCMT.write('DBI0')  # sweep bias 0A
set_pulse_timing(HOLD_TIME, MEAS_DELAY, PERIOD)
set_sweep(START_CURR, 0, STEP_CURR)
ADCMT.write('ST1,RL') # memory store on & memory clear
ADCMT.write('OPR') # output on
ADCMT.write('*TRG') # sweep start
sleep(10)
ADCMT.write('SBY')  # output off
set_pulse_timing(HOLD_TIME, MEAS_DELAY, PERIOD)
set_sweep(0, STOP_CURR, STEP_CURR)
ADCMT.write('ST1,RL') # memory store on & memory clear
ADCMT.write('OPR') # output on
ADCMT.write('*TRG') # sweep start
sleep(10)
ADCMT.timeout = 2000  # Acquisition timeout in milliseconds - set it higher than the acquisition time
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition

ADCMT.write('SBY')  # output off
ADCMT.query('*OPC?')

ADCMT.close()
