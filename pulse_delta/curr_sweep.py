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
DELTA_DELAY = 100e-6
PULSE_WIDTH = 500e-6
DELTA_COUNT4MEAS = 10
TRACE_POINT4MEAS = 10
DELTA_COUNT4FLIP = 2
TRACE_POINT4FLIP = 2
FLIP_TIME = 5
MEAS_TIME = 5
CURR_LOW = 0 # 0-CURR_HIGH pulse

CURR_4_SWICH = -20e-3

CURR_MIN_0 = 0
MEAS_POINT_NUM_0 = 11
CURR_DELTA_0 = 2.00E-03

CURR_MIN_1 = 24e-3
MEAS_POINT_NUM_1 = 25
CURR_DELTA_1 = -2.00E-03


SOURCE_MEAS_CURR = 100e-6
# -----------------------------------------------------------
# Measurement
# -----------------------------------------------------------
ke_6221.write('*RST')
# Nanovol settings via 6221
# ke_6221.write('SYST:COMM:SER:SEND \"VOLT:RANG 0.1\"')
# sleep(1)
# ke_6221.write('SYST:COMM:SER:SEND \"VOLT:NPLC 0.1\"')
# sleep(1)

ke_6221.write('UNIT VOLTS')
ke_6221.write('SOUR:PDEL:RANG BEST')
ke_6221.write('SOUR:PDEL:INT 5')
ke_6221.write('SOUR:PDEL:SWE OFF')
ke_6221.write('SOUR:PDEL:LME 2')
ke_6221.write('SOUR:PDEL:LOW %f' % CURR_LOW)
ke_6221.write('SOUR:PDEL:WIDT %f' % PULSE_WIDTH)
ke_6221.write('SOUR:PDEL:SDEL %f' % DELTA_DELAY)

print("Initialization")
print("source_current average_voltage_for_flip average_voltage_for_meas")
source_curr = CURR_4_SWICH
ke_6221.write('SOUR:PDEL:HIGH %f' % source_curr)
ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4FLIP)
ke_6221.write('TRAC:POIN %d' % TRACE_POINT4FLIP)
ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
ke_6221.write('INIT:IMM') # starts delta measurements
sleep(FLIP_TIME) # wait until measurement stops
ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
read_data_flip_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
meas_data_flip_volt = read_data_flip_volt[::2]

ke_6221.write('SOUR:PDEL:HIGH %f' % SOURCE_MEAS_CURR)
ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4MEAS)
ke_6221.write('TRAC:POIN %d' % TRACE_POINT4MEAS)
ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
ke_6221.write('INIT:IMM') # starts delta measurements
sleep(MEAS_TIME) # wait until measurement stops
ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
read_data_meas_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
meas_data_meas_volt = read_data_meas_volt[::2]
print('{:.8f}'.format(source_curr), numpy.average(meas_data_flip_volt), numpy.average(meas_data_meas_volt))

print("seq0")
print("source_current average_voltage_for_flip average_voltage_for_meas")
for meas_point in range(MEAS_POINT_NUM_0):
    source_curr = CURR_MIN_0 + meas_point * CURR_DELTA_0
    ke_6221.write('SOUR:PDEL:HIGH %f' % source_curr)
    ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4FLIP)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4FLIP)
    ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(FLIP_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_flip_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_flip_volt = read_data_flip_volt[::2]

    ke_6221.write('SOUR:PDEL:HIGH %f' % SOURCE_MEAS_CURR)
    ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4MEAS)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4MEAS)
    ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(MEAS_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_meas_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_meas_volt = read_data_meas_volt[::2]
    print('{:.8f}'.format(source_curr), numpy.average(meas_data_flip_volt), numpy.average(meas_data_meas_volt))

print("seq1")
print("source_current average_voltage_for_flip average_voltage_for_meas")
for meas_point in range(MEAS_POINT_NUM_1):
    source_curr = CURR_MIN_1 + meas_point * CURR_DELTA_1
    ke_6221.write('SOUR:PDEL:HIGH %f' % source_curr)
    ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4FLIP)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4FLIP)
    ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(FLIP_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_flip_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_flip_volt = read_data_flip_volt[::2]

    ke_6221.write('SOUR:PDEL:HIGH %f' % SOURCE_MEAS_CURR)
    ke_6221.write('SOUR:PDEL:COUN %d' % DELTA_COUNT4MEAS)
    ke_6221.write('TRAC:POIN %d' % TRACE_POINT4MEAS)
    ke_6221.write('SOUR:PDEL:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(MEAS_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data_meas_volt = ke_6221.query_ascii_values("trace:data?") # even: meas_data_flip_volt, odd:  meas_time
    meas_data_meas_volt = read_data_meas_volt[::2]
    print('{:.8f}'.format(source_curr), numpy.average(meas_data_flip_volt), numpy.average(meas_data_meas_volt))

ke_6221.close()
