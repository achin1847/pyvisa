
import visa
import matplotlib.pyplot as plt
#import VISAresourceExtentions

# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
rm.list_resources()
ADCMT = rm.open_resource('GPIB0::1::INSTR') # ADC Corp.,6241A,154080243,D00
print(ADCMT.query('*IDN?'))

ADCMT.write('*RST;*CLS')
# -----------------------------------------------------------
# Mode Settings:
# ----------------------------------------------------------
ADCMT.write('OH1') # header on
ADCMT.write('M1')  # trigger mode hold
ADCMT.write('VF')  # voltage output
ADCMT.write('F2')  # current measurement
ADCMT.write('MD1')  # pulse gen
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
# for count in range(10):
ADCMT.write('SOV2,LMI0.003')  # pulse 2V, limit 3mA
ADCMT.write('DBV1')  # pulse base 1V
ADCMT.write('SP3,1,130,50')  # hold time: 3ms, masure delay: 1ms, period: 130ms, pulse time 50ms
ADCMT.write('OPR') # output on
ADCMT.timeout = 2000  # Acquisition timeout in milliseconds - set it higher than the acquisition time
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')  # Using *OPC? query waits until the instrument finished the acquisition

ADCMT.write('SOV2.5')  # pulse 2.5V
ADCMT.write('SP3,60,130,50')  # hold time: 3ms, masure delay: 60ms, period: 130ms, pulse time 50ms
ADCMT.timeout = 2000
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')

ADCMT.write('DBV0.5')  # pulse base 0.5V
ADCMT.timeout = 2000
print('Waiting for the acquisition to finish... ')
ADCMT.query('*OPC?')

ADCMT.write('SBY')  # output off
ADCMT.query('*OPC?')

ADCMT.close()
