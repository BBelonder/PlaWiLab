#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import time
import datetime
from drivers import TDS2000b,xgs600
#import drivers

#	To Do List:
#		Choose between devices, only use those which are connected
#		Make out_line responsive to the active, read out channels
def getIDs():
	"""
	asks for Vendor and Product IDs
	"""
	global VendorID
	global ProductID
	global port
	VendorID=int(input("VendorID? Hex must start with 0x! Use lsusb in terminal to find your VID PID "),0) # hex geht so auch
	ProductID=int(input("ProductID? Hex must start with 0x! "),0)
	port=input("Which /dev/ is your usb to serial bridge on? Use 'dmesg | grep tty' to find it. Input must have form '/dev/ttyUSBX' ")


def startline(self):
	"""
	Defines the first line of output
	"""
	startformat=["Time (t)"]
	startline="{0:>8s}"
	for ch in self.readChannels():
		startline+=";{"+str(ch)+":>8s}"
		startformat.append("CH"+str(ch)+" ("+self.ReadUnit()[ch]+")")
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
#	print("Filename will be: "+a)
	return a

def set_folder():
	"""
	Defines the folder where the data will be stored
	"""
	folder=str(input("Where do you want to save your data? Folder must be given in str format. "))
	global outp
	print("Data will be saved to "+folder+"/"+filename())
	outp=open(folder+"/"+filename(),"w")
	
def write_line():
	"""
	writes line into file, yet fixed on device "Oszi", not done yet
	"""
	max_time=int(input("How long am I supposed to track data? (s)"))
	start_time=time.time()
	global current_time
	current_time=0
	while current_time <= max.time:
		b=Oszi.ReadChanSingleValues()
		out_line=[current_time]
		for ch in Oszi.readChannels():
			outline.append(Oszi)
		current_time=time.time()-start_time
	

if __name__=="__main__":
	set_folder()	
	getIDs()
	Oszi=TDS2000b.TDS2000bDriver(VendorID,ProductID)
	Oszi.SetChannels(1,2)
	Oszi.SetWidth(1)
	print(Oszi.readChannels())
	#print(Oszi.__dict__)
	#outp=open("/home/pi/LabData/"+filename(),"w")
	#print(startline(Oszi))

	outp.write(startline(Oszi))
	max_time=int(input("Wie lange soll ich jetzt aufzeichnen? "))
	start_time=time.time()
	a=0
	while a <= max_time:
		a=time.time()-start_time
		b=Oszi.ReadChanSingleValues()
		#print(b)
		out_line="{0:8.3f};{1:9.6f};{2:9.6f}\n".format(a,b[0],b[1])
		outp.write(out_line)
		#time.sleep(0.3) #ohne die Begrenzung immerhin ne Messung alle 0.2s!
	
	outp.close()
