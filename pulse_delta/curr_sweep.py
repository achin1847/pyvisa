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
DELTA_COUNT4MEAS = 10
TRACE_POINT4MEAS = 10
DELTA_COUNT4FLIP = 1
TRACE_POINT4FLIP = 1
FLIP_TIME = 3
MEAS_TIME = 5
CURR_MIN = 100e-6
MEAS_POINT_NUM = 5
CURR_DELTA = 10e-6
SOURCE_MEAS_CURR = 100e-6
# -----------------------------------------------------------
# Measurement
# -----------------------------------------------------------
ke_6221.write('*RST')
ke_6221.write('UNIT VOLTS')
ke_6221.write('SOUR:DELT:DELay %f' % DELTA_DELAY)
ke_6221.write('SOUR:DELT:CAB ON')

print("source_current average_voltage(flip) average_voltage(measurement)")
for meas_point in range(MEAS_POINT_NUM):
    source_curr = CURR_MIN + meas_point * CURR_DELTA
    ke_6221.write('SOUR:DELT:HIGH %f' % source_curr)
    ke_6221.write('SOUR:DELT:COUN %d' % DELTA_COUNT4FLIP)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4FLIP)
    ke_6221.write('SOUR:DELT:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(FLIP_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_flip_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_flip_volt = read_data_flip_volt[::2]

    ke_6221.write('SOUR:DELT:HIGH %f' % SOURCE_MEAS_CURR)
    ke_6221.write('SOUR:DELT:COUN %d' % DELTA_COUNT4MEAS)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4MEAS)
    ke_6221.write('SOUR:DELT:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(MEAS_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_meas_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_meas_volt = read_data_meas_volt[::2]

    print('{:.8f}'.format(source_curr), numpy.average(meas_data_flip_volt), numpy.average(meas_data_meas_volt))

ke_6221.close()
