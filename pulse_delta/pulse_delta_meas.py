# -----------------------------------------------------------
# Author: Akiyo
# Description: Example for pulse delta measurement
# Required equipments: Keithley6221 Current Source
#                      Keithley2182A nanovoltmeter
#                      RS232-cable
#                      Trigger Link cable
# Reference: Reference Manual 622x-901-01 Rev. C / October 2008
# -----------------------------------------------------------
import visa
import matplotlib.pyplot as plt
from time import sleep
import numpy
# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ke_6221 = rm.open_resource('GPIB0::12::INSTR') # KEITHLEY6221
# -----------------------------------------------------------
# Constants
# -----------------------------------------------------------
DELTA_DELAY = 100e-3
DELTA_COUNT = 10
TRACE_POINT = 10
MEAS_TIME = 5
# -----------------------------------------------------------
# Measurement
# -----------------------------------------------------------
ke_6221.write('*RST')
ke_6221.write('UNIT OHMS')
ke_6221.write('SOUR:DELT:DELay %f' % DELTA_DELAY)
ke_6221.write('SOUR:DELT:COUN %d' % DELTA_COUNT)
ke_6221.write('SOUR:DELT:CAB ON')
ke_6221.write('TRAC:POIN %d' % TRACE_POINT)
for meas_point in range(1, 10):
    source_curr = meas_point * 1e-6
    ke_6221.write('SOUR:DELT:HIGH %f' % source_curr)
    ke_6221.write('SOUR:DELT:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(MEAS_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data = ke_6221.query_ascii_values("trace:data?") # even: meas_data, odd:  meas_time
    meas_data = read_data[::2]
    print("source_current, avg_meas_data:", source_curr, numpy.average(meas_data))

ke_6221.close()
