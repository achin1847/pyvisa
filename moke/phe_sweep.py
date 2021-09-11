
import visa
import matplotlib.pyplot as plt
import numpy as np
import time
usleep = lambda x: time.sleep(x/1000000.0)

# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ADCMT = rm.open_resource('GPIB0::27::INSTR') # ADC Corp.,6240A,154080243,D00
print(ADCMT.query('*IDN?'))

ADCMT.write('*RST;*CLS')
# -----------------------------------------------------------
# Mode Settings:
# ----------------------------------------------------------
ADCMT.write('OH1') # header on
ADCMT.write('M1')  # trigger mode hold
ADCMT.write('IF')  # current output
ADCMT.write('F1')  # voltage measurement
# -----------------------------------------------------------
# Constants of ADCMT 6240A
# -----------------------------------------------------------
MAG_CURR_MIN_P = 0.02
MEAS_POINT_NUM_P = 401
MAG_CURR_DELTA_P = -0.0005

MAG_CURR_MIN_M = -0.02
MEAS_POINT_NUM_M = 201
MAG_CURR_DELTA_M = 0.0001
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
ADCMT.write('SOI0,LMV3')  # pulse 0mA, limit 3V
ADCMT.write('OPR') # output on

for loop in range(3):
    for meas_point in range(MEAS_POINT_NUM_P):
        mag_curr = MAG_CURR_MIN_P + meas_point * MAG_CURR_DELTA_P
        ADCMT.write('SOI%f' % mag_curr)
        usleep(1000)

    for meas_point in range(MEAS_POINT_NUM_M):
        mag_curr = MAG_CURR_MIN_M + meas_point * MAG_CURR_DELTA_M
        ADCMT.write('SOI%f' % mag_curr)
        usleep(1000)

print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition


# ADCMT.write('SBY')  # output off
ADCMT.query('*OPC?')

ADCMT.close()
