
import pyvisa as visa
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
    ADCMT.write('SN%f,%f,%f' % (start, stop, step))

def set_pulse_timing(hold_time, meas_delay, period):
    """
    set pulse timing for ADCMT

    Parameters
    ----------
    hold_time (ms)  : Th
    meas_delay (ms) : Td
    period (ms)     : Tp
    """
    ADCMT.write('SP%f,%f,%f' % (hold_time, meas_delay, period))
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
START_CURR = -0.02 #A
STOP_CURR = 0.02 #A
# STEP_CURR = 0.0002 #A

# HOLD_TIME = 1 #ms
STEP_CURR_MIN = 0.00002 #A
step_curr_point = STEP_CURR_MIN
STEP_CURR_DELTA = 0.00001
STEP_CURR_POINT_NUM = 11

HOLDTIME_MIN = 1 #ms
hold_time = HOLDTIME_MIN
HOLD_POINT_NUM = 1
HOLDTIME_DELTA = 1
MEAS_DELAY = 4 #ms
PERIOD = hold_time + MEAS_DELAY + 5 #ms
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
ADCMT.write('LMV3')  # limit 3V
ADCMT.write('DBI0')  # sweep bias 0A
for step_curr_point in range(STEP_CURR_POINT_NUM):
    step_curr = STEP_CURR_MIN + step_curr_point * STEP_CURR_DELTA
    for hold_point in range(HOLD_POINT_NUM):
        hold_time = HOLDTIME_MIN + hold_point * HOLDTIME_DELTA
        set_pulse_timing(hold_time, MEAS_DELAY, PERIOD)
        set_sweep(START_CURR, STOP_CURR, step_curr)
        ADCMT.write('ST1,RL') # memory store on & memory clear
        ADCMT.write('OPR') # output on
        ADCMT.write('*TRG') # sweep start
        sleep(60)
        ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition
        ADCMT.write('SBY')  # output off

ADCMT.close()
