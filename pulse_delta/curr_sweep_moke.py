# -----------------------------------------------------------
# Author: Akiyo
# Description: Example for pulse delta measurement
# Required equipments: Keithley6221 Current Source
#                      Keithley2182A nanovoltmeter
#                      RS232-cable
#                      Trigger Link cable
# Reference: Reference Manual 622x-901-01 Rev. C / October 2008
# -----------------------------------------------------------
import pyvisa as visa
import matplotlib.pyplot as plt
from RsInstrument.RsInstrument import RsInstrument, BinFloatFormat
from time import sleep
import numpy
# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ke_6221 = rm.open_resource('GPIB0::12::INSTR') # KEITHLEY6221
# ke_6221.read_termination = '\r'
# -----------------------------------------------------------
# Constants
# -----------------------------------------------------------
DELTA_DELAY = 500e-6
PULSE_WIDTH = 550e-6
DELTA_COUNT4MEAS = 1
TRACE_POINT4MEAS = 1
DELTA_COUNT4FLIP = 1
FLIP_TIME = 2

CURR_LOW = 0 # 0-CURR_HIGH pulse

CURR_MIN_0 = 25E-03
MEAS_POINT_NUM_0 = 2
CURR_DELTA_0 = -50E-03


CURR_MIN_1 = 0
MEAS_POINT_NUM_1 = 1
CURR_DELTA_1 = 20E-03

# -----------------------------------------------------------
# Measurement
# -----------------------------------------------------------
ke_6221.write('*RST')

ke_6221.write('UNIT VOLTS')
ke_6221.write('SOUR:PDEL:RANG BEST')
ke_6221.write('SOUR:PDEL:INT 5')
ke_6221.write('SOUR:PDEL:SWE OFF')
ke_6221.write('SOUR:PDEL:LME 2')
ke_6221.write('SOUR:PDEL:LOW %f' % CURR_LOW)
ke_6221.write('SOUR:PDEL:WIDT %f' % PULSE_WIDTH)
ke_6221.write('SOUR:PDEL:SDEL %f' % DELTA_DELAY)

print("seq0")
print("source_current average_voltage_for_flip average_voltage_for_meas")
for meas_point in range(MEAS_POINT_NUM_0):
    source_curr = CURR_MIN_0 + meas_point * CURR_DELTA_0
    ke_6221.write('SOUR:PDEL:HIGH %f' % source_curr)
    ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4FLIP)
    ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(FLIP_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_flip_volt = ke_6221.query_ascii_values("SENS:DATA?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_flip_volt = read_data_flip_volt[::2]

    print('{:.8f}'.format(source_curr), numpy.average(meas_data_flip_volt))



ke_6221.close()
