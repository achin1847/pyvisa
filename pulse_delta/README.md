# PyVISA pulse delta measurement
## Environment
- Keithley6221 Current Source
- Keithley2182A nanovoltmeter
- RS232-cable
- Trigger Link cable

### Reference:
- [Reference Manual 622x-901-01 Rev. C / October 2008](https://jp.tek.com/product-series/ultra-sensitive-current-sources-series-6200-manual-0)
  - p. 124 - Delta, Pulse Delta, and Differential Conductance

## How to run pulse delta measurement
### Instruments Settings
1. Connect RS232-cable between 6221 and 2182A
2. Connect Trigger Link cable between 6221 and 2182A
3. Connect GPIB cable between 6221 and PC
4. Guarding Setting
  - On 6221, press the TRIAX key
  - Select GUARD or OUTPUT LOW (220 STYLE) and press the ENTER key
  - Press the EXIT key
5. **2182A** communication Setting
  - Press shift key > RS-232 key
  - Select ON for the RS-232 interface
  - Select the 19.2K baud rate
  - Select the NONE setting for flow control
  - **Important Notice**
    - When 2182A is set with RS-232 communication mode, it cannot be recognized by GPIB. The setting is retained even if the power is turned off.
    - After the measurement is completed, **please select OFF** for the RS-232 interface on 2182A.
6. **6221** RS-232 communication Setting
  - Press COMM key > select RS-232
  - Make sure 6221 reboots and the baud rate is set as 19.2K
7. **6221** GPIB communication Setting
  - Press COMM key > select GPIB
  - Make sure 6221 reboots

### Example of how to run script
1. Download scripts
```
$ git clone https://github.com/achin1847/pyvisa.git
$ cd pyvisa/example/
```
2. Please confirm that 6221 can be recognized and GPIB number
```
$ python3 inq_inst.py
(GPIB0::12::INSTR')
KEITHLEY INSTRUMENTS INC.,MODEL 6221
```
3. Run a pulse delta measurement script (example)
  - Optional: fix *.py if the GPIB0 number is not GPIB0::12::INSTR
```
$ cd ../pulse_delta/
$ python3 curr_sweep.py
```
