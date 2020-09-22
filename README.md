# Control measurement instruments using PyVISA
PyVISA is a Python package for support of the "Virtual Instrument Software Architecture" (VISA), which enables to control measurement instruments via GPIB, RS232, Ethernet, or USB.
Scripts in this repository can be utilized instead of LabVIEW programs.
## Environment
- macOS Catalina 10.15.6
- Python 3.7.6
- PyVISA 1.10.1（pip3 install pyvisa）
- PySerial 3.4（pip3 install pyserial）
- NI-GPIB 19.5
- NI-VISA Runtime 19.0.0
- RsInstrument 1.4.0.29 (pip install Rsinstrument)

### References:
- [PyVISA](https://pyvisa.readthedocs.io/en/latest/)
- [macOS Catalina で PyVISA/PySerial を使う](https://oxon.hatenablog.com/entry/2020/06/09/175343)

## Example of using PyVISA
### Find instruments and query the information
- inq_inst.py - find GPIB number and the information of instruments
```
$ git clone https://github.com/achin1847/pyvisa.git
$ cd pyvisa/example/
$ python inq_inst.py
('GPIB0::1::INSTR', 'GPIB0::14::INSTR')
GPIB0::1::INSTR
ADC Corp.,R6240A,440300035,B01
GPIB0::14::INSTR
KEITHLEY INSTRUMENTS INC.,MODEL 2000,4017569,B01  /A02
```

### For individual instrument control
- adcmt_6241A.py - control script for ADCMT 6241A
- rto_1044.py - control script for Rohde&Schwarz RTO1044
### References:
- [Rohde&Schwarz Getting Started](https://www.rohde-schwarz.com/jp/driver-pages/remote-control/getting-started_231558.html)
- [R&S®RTO1000 User Manual](https://www.rohde-schwarz.com/cz/manual/r-s-rto1000-user-manual-manuals-gb1_78701-29054.html)
- [6241A / 6242 manual](https://www.adcmt.com/products/vig/6241/download)
