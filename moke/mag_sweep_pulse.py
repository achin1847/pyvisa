
import visa
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------
# Function
# -----------------------------------------------------------
# def get_nearest_value_index(list, num):
#     idx = np.abs(np.asarray(list) - num).argmin()
#     return idx
# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ADCMT = rm.open_resource('GPIB0::1::INSTR') # ADC Corp.,6240A,154080243,D00
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
# Trigger Settings:
# -----------------------------------------------------------
ADCMT.write('SOI0.003,LMI3')  # pulse 3mA, limit 3V
ADCMT.write('DBI0')  # pulse base 0A
ADCMT.write('SP3,1,130,50')  # hold time: 3ms, masure delay: 1ms, period: 130ms, pulse time 50ms
ADCMT.write('OPR') # output on
ADCMT.timeout = 2000  # Acquisition timeout in milliseconds - set it higher than the acquisition time
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition


ADCMT.write('SBY')  # output off
ADCMT.query('*OPC?')

ADCMT.close()
