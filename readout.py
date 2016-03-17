#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import time
import datetime
from drivers import TDS2000b,xgs600
#import drivers

#def __init__():
#	"""
#	general purpose for this tool
#	"""
#	getIDs()
#	Oszi=TDS2000b.TDS2000bDriver(VendorID,ProductID)
#	XGS=XGS600Driver()
	
def getIDs():
	"""
	asks for Vendor and Product IDs
	"""
	global VendorID
	global ProductID
	VendorID=int(input("VendorID? Hex Numbers must start with '0x'. Use lsusb in terminal to find your VID PID "),0) # hex wokrs thanks ",0"
	ProductID=int(input("ProductID? Hex Numbers must start with '0x'. "),0)
# use 'dmesg | grep tty' to find the dev path of the serial to usb bridge to communicate with xgs600	


def startline(self):
	"""
	Defines the first line of output
	"""
	startformat=["Time [t]"]
	startline="{0:>8s}"
	
	for ch in self.readChannels():
		startline+=";{"+str(ch)+":>8s}"
		startformat.append("CH"+str(ch))
		print(startline)
		print(startformat)
	startline+="\n"
	#print(startline.format(*startformat))
	return startline.format(*startformat)
	
def filename():
	"""
	Defines the Filename to current date and time.txt
	"""
	i=datetime.datetime.now()
	a="{0:02d}-{1:02d}-{2:02d}--{3:02d}.{4:02d}.txt".format(i.year,i.month,i.day,i.hour,i.minute)
	print("Filename will be: "+a)
	return a

getIDs()
Oszi=TDS2000b.TDS2000bDriver(VendorID,ProductID)
Oszi.SetChannels(1,2)
print(Oszi.readChannels())
#print(Oszi.__dict__)
outp=open(filename(),"w")
CH=Oszi.readChannels()
print(CH)
print(startline(Oszi))

outp.write(startline(Oszi))#Channel aus Oszi einlesen
max_time=int(input("Wie lange soll ich jetzt aufzeichnen? "))
start_time=time.time()
a=0
while a <= max_time: #time.time()-start_time <= max_time:
	a=time.time()-start_time
	b=Oszi.ReadChanSingleValues()
	print(b)
	out_line="{0:8.3f};{1:9.6f};{2:9.6f}\n".format(a,b[0],b[1])
	outp.write(out_line)
	#time.sleep(0.3) #ohne die Begrenzung immerhin ne Messung alle 0.2s!
	#a+=.2
	
outp.close()
