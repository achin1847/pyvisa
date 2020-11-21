# -----------------------------------------------------------
# Author: Akiyo
# Description: R vs field (pulse delta measurement)
# Required equipments: Keithley6221 Current Source
#                      Keithley2182A nanovoltmeter
#                      ADCMT 6240A Current/Voltage Source
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
adc_6240 = rm.open_resource('GPIB0::1::INSTR') # ADC Corp.,6240A
# -----------------------------------------------------------
# Constants of ADCMT 6240A
# -----------------------------------------------------------
MAG_VOL_MIN = -0.1
MEAS_POINT_NUM = 10
MAG_VOL_DELTA = 0.01
# -----------------------------------------------------------
# Constants of KEITHLEY6221
# -----------------------------------------------------------
DELTA_DELAY = 100e-3
DELTA_COUNT = 10
TRACE_POINT = 10
MEAS_TIME = 3 # sec
SOURCE_CURR = 1e-6
# -----------------------------------------------------------
# Settings of ADCMT 6240A
# -----------------------------------------------------------
adc_6240.write('C,*RST')
adc_6240.write('M1')  # trigger mode hold
adc_6240.write('VF')  # voltage output
adc_6240.write('F2')  # current measurement
adc_6240.write('SOV0,LMI0.003')  # dc 0V, limit 3mA
adc_6240.write('OPR') # output on
# -----------------------------------------------------------
# Settings of KEITHLEY6221
# -----------------------------------------------------------
ke_6221.write('*RST')
ke_6221.write('UNIT OHMS')
ke_6221.write('SOUR:DELT:DELay %f' % DELTA_DELAY)
ke_6221.write('SOUR:DELT:COUN %d' % DELTA_COUNT)
ke_6221.write('SOUR:DELT:CAB ON')
ke_6221.write('TRAC:POIN %d' % TRACE_POINT)
ke_6221.write('SOUR:DELT:HIGH %f' % SOURCE_CURR)
# -----------------------------------------------------------
# Measurement
# -----------------------------------------------------------
print("voltage_of_magnet average_resistance")
for meas_point in range(MEAS_POINT_NUM):
    mag_vol = MAG_VOL_MIN + meas_point * MAG_VOL_DELTA
    adc_6240.write('SOV%f' % mag_vol)
    ke_6221.write('SOUR:DELT:ARM') # arms delta mode
    ke_6221.write('INIT:IMM') # starts delta measurements
    sleep(MEAS_TIME) # wait until measurement stops
    ke_6221.write('SOUR:SWE:ABOR') # stops delta mode
    read_data = ke_6221.query_ascii_values("trace:data?") # even: meas_data, odd:  meas_time
    meas_data = read_data[::2]
    print('{:.2f}'.format(mag_vol), numpy.average(meas_data))

adc_6240.write('SBY')  # output off
adc_6240.query('*OPC?')

ke_6221.close()
adc_6240.close()
