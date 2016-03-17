#!/usr/bin/env python
# encoding: utf-8

#from __future__ import print_function
import usbtmc
import time

class TDS2000bDriver():
	"""
	Class TDS2000bDriver provides a driver(?) for the useage of python to 
	readout a Tektronix TDS2000b+ Oszilloscope
	Commands used should also work for TDS200, TDS1000/2000 and TPS2000
	"""
	
	def __init__(self,VendorID,ProductID,StartP=1250,EndP=1250):
		"""
		By Default 4 Channels are active self.__Channels=[1,2,3,4].
		Use self.SetChannels(**Channels) to modify active Channel list
		Vendor ID and ProductID may be given in hex or dec
		Enc is signed Ascii by default. If you change that, you'll have 
		to adjust self.__widthD yourself.
		"""
		self.set_Oszi(VendorID,ProductID,StartP=1250,EndP=1250)
		
	def set_Oszi(self,VendorID,ProductID,StartP=1250,EndP=1250):
		"""
		By Default 4 Channels are active self.__Channels=[1,2,3,4].
		Use self.SetChannels(**Channels) to modify active Channel list.
		Vendor ID and ProductID, in dec. hex values mus start with 0x.
		Enc is signed Ascii by default. If you change that, you'll have 
		to adjust self.__widthD yourself.
		"""
		self.__VID=VendorID
		self.__PID=ProductID
		self.__dev=usbtmc.Instrument(VendorID,ProductID)
		self.SetStartPoint(StartP)
		self.SetEndPoint(EndP)
		self.__Channels=[1,2,3,4]
		self.__voltsDiv={}
		self.voltsDiv()
		self.__widthD={1:127,2:32767}
		self.__width=2
		self.SetEncAscii()
		
	def SetEncAscii(self):
		"""
		Sets Encoding to Ascii
		"""
		self.write("Data:Encdg ASCII")
		
	def voltsDiv(self):
		"""
		Reads the Volts/Div parameter from the oszi and returns it as
		a property of self
		"""
		self.__voltsDiv=dict.fromkeys(self.__Channels)
		for n in self.__Channels:
			setting=self.ask("CH"+str(n)+"?")
			self.__voltsDiv[n]=float(setting.split(";")[2]) #reads out volts/div Settings from oszi
		
	def ask(self,query):
		"""
		Hands given query to the oszilloscope
		"""
		if type(query) == str:
			answ=self.__dev.ask(query)
			return answ
		else:
			raise TypeError("Queries must be given in ''.")

	def write(self,order):
		"""
		Hands given order to the oszilloscope
		"""
		if type(order) == str:
			self.__dev.write(order)
		else:
			raise TypeError("Orders must be given in ''.")
			
	def SetChannels(self,*Channels):
		"""
		Sets active Channels
		"""	
		self.__Channels=[]
		for i in Channels:
			self.__Channels.append(i)
		self.__Channels.sort()
		print("Active Channels have been set to "+str(self.__Channels))
		
	def readChannels(self):
		"""
		Reads active Channels
		"""
		return self.__Channels
		
	def read_cur_Value(self):
		"""
		reads the current Values of active Channels
		"""
		
	def SetStartPoint(self,startp):
		"""
		Sets Startpoint for Data Aquisiton, Range for TDS2004b is 1-2500
		"""
		self.write("Data:Start "+str(startp))
		self.__startP=startp
		
	def ReadStartPoint(self):
		"""
		Reads current Startpoint for DataAquisiton
		"""
		return self.ask("Data:Start?")
		
	def SetEndPoint(self,endp):
		"""
		Sets Endpoint for Data Aquisiton, Range for TDS2004b is 1-2500
		"""
		self.write("Data:End "+str(endp))
		self.__endP=endp
		
	def ReadEndPoint(self):
		"""
		Reads current Endpoint for DataAquisiton
		"""
		return self.ask("Data:Start?")
		
	def SetSource(self,Channel):
		"""
		Sets Source for Data Aquisition
		"""
		if Channel not in self.__Channels:
			#raise TypeError("The channel needs to be activated first")
			inp=str(input("The Channel is not yet activated. To you wish to do so? y|n "))
			if inp == "y":
				self.SetChannels(Channel)
				self.write("Data:source CH"+str(Channel))
				return "Channel "+str(Channel)+" has been activated and is now source for data"
			else:
				raise TypeError("Cannot read from inactive Channel")
		else:
			self.write("Data:source CH"+str(Channel))
			return "Source was set to channel"+str(Channel)
		
	def ReadSource(self):
		"""
		Reads current Source for Data Aquisition
		"""
		return self.ask("Data:source?")
	
	def SetWidth(self,width):
		"""
		Sets aquistion width, 1 equals -128 to 127, 2 equals -32768 to 32767
		"""
		self.write("Data:width "+str(width))
		
	def ReadChanSingleValues(self):
		"""
		Reads the single Values for the active Channels	and StartP,EndP
		returns List with Values for each Channel in sorted order
		"""
		val=[]
		for n in self.__Channels:
			self.SetSource(n)
			val.append(int(self.ask("Curve?"))/self.__widthD[self.__width]*5*self.__voltsDiv[n])
			#die self.__withD-Konstruktion ist nötig, um die übertragungsbreiten bei der Bestimmung
			#des Bereichs zu berücksichtigen
		return val
		
if __name__=="__main__":
	start_time=time.time()
	x=TDS2000bDriver(1689,869)#check
	print(x.ask("*IDN?"))#check
	print(x.__dict__)#check
	x.SetChannels(1,2)#check
	print(x.readChannels())#check	
	print(x.ReadChanSingleValues())
#	x.SetChannels(2,3,1)
#	print(x.ReadChanSingleValues())
#	x.SetChannels(3)#check
#	print("Active Channels have been set to 3")#check
#	print(x.readChannels())#check
#	print("Current Startpoint is at",x.ReadStartPoint())#check
#	print("Setting Startpoint to 1251")#check
#	x.SetStartPoint(1251)#check
#	print("Current Startpoint is at",x.ReadStartPoint())#check
#	print(x.ReadSource()) #check
#	print(x.SetSource(3)) #check
#	print(x.ReadSource()) #check
	passed_time=time.time()-start_time
	print("{0:03.3f} Sekunden hat's gedauert".format(time.time()-start_time))

"""
To Do List:

Invertierung berücksichtigen! is setting.split(";")[-2] (vgl. divVolts): ON/OFF

Irgendwie schauen, dass man nicht aktive Kanäle (am Oszi) rauswirft, sonst
kann man die der Channellist hinzufügen und das Programm schmiert ab

"""
