This is but a humble attempt to creat a script, that reads Values from an Tektronix TDS2004b Oscilloscope and pressures from a XGS600 Controller and writes them into a file.

It includes a driver for the XGS600, which was taken from github.com/CINF/PyExpLabSys

The Driver for the TDS2004b is work in progess and by now specified to read only the central datapoint of each channel. Work is now concentrating on the usage of measurement:immed method for TDS2000-family. Should work faster than the older method. But still work in progress.
