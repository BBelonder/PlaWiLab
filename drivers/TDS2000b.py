#!/usr/bin/env python
# encoding: utf-8

#from __future__ import print_function
import usbtmc
import time
import ast

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
		Work in Progress: The measurement methods are now being 
		implemented, aim is to archieve better time resolution
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
		self.__unitD={}
		self.ReadUnit()
		self.__Offset={}
		self.Offset()
		self.__Inv={}
		self.ReadInv()
		#self.SetImmedTypes("MEAN")
		self.__IMMESrcD=dict.fromkeys(range(1,5))
		self.__IMMETypD=dict.fromkeys(range(1,5))
		self.__IMMEUniD=dict.fromkeys(range(1,5))
		self.ReadImmedUnits()
		self.__IMMEValD=dict.fromkeys(range(1,5))
		#self.

	def SetImmedTypes(self,Type):
		"""
		Sets Type of immed measurement. Type can be: FREQ, MEAN, PERI, 
		PK2pk, MINI, MAXI, RIS, FALL, PWI, NWI, CRM. See TDS Programmer's
		Manual p2-158ff.
		"""
		for n in self.__IMMETypeD:
			self.write("measurement:immed:type "+str(Type))
			self.__IMMETypeD[n]=str(Type)
		return self.__IMMETypeD
		
	def SetImmedType(self,key,ch,Type):
		"""
		Sets the type for a specific key in the readout procedure
		"""
		self.__IMMETypD[key]=Type
		while type(ch)!=int:
			ch=ast.literal_eval(input("Please only give channel number! "))
				
		self.__IMMESrcD[key]=ch		
		
	def GetImmedValues(self):
		"""
		Grabs the immed values and puts them into dict
		"""
		self.__IMMEValD={}
		for n in self.__IMMETypD:
			self.write("measurement:immed:type "+str(self.__IMMETypD[n])+";Source "+str(self.__IMMESrcD[n]))
			self.IMMEValD[n]=self.ask("measurement:immed:value?")
		
	def ReadImmedSrcs(self):
		"""
		Reads current Source for Immed measurement
		"""
		return self.__IMMESrcD
		
	def AddImmedSrc(self,key,Src):
		"""
		Adds/replaces Source for immed measurement		
		"""
		while Src not in [CH1,CH2,CH3,CH4,"CH1","CH2","CH3","CH4"]:
			Src=ast.literal_eval(input("Please repeat your input in terms of 'CHx' :"))	
		d={key:str(Src)}
		self.__IMMESrcD.update(d)
		return str(Src)+" has been added to readout routine. Key for this Channel is "+str(key)
		
	def AddImmedSrcs(self,keys,srcs):
		"""
		Adds/replaces several 
		"""
		while len(keys)!=len(srcs):
			print("The number of keys does not match the number of sources!\n")
			keys=ast.literal_eval(input("Please enter your keys again: "))
			srcs=ast.literal_eval(input("Pleas enter your sources again: "))
		for n in range(len(src)):
			if src[n] in [CH1,CH2,CH3,CH4,"CH1","CH2","CH3","CH4"]:
				pass
			else:
				print("The Channels must be given in Terms of 'CHx'\n")
				src[n]=str(ast.literal_eval(input("Please repeat the Channel to key no."+str(key[n]))))		
		self.__IMMESrcD=dict(zip(keys,srcs))
		return self.__IMMESrcD
		
		
	def ReadImmedUnits(self):
		"""
		Reads the Units from the immed measurement and puts them into
		__IMMEUnitD. Returns the dict.
		"""
		for n in self.__IMMEUnitD:
			self.__IMMEUnitD[n]=self.ask("measurment:immed:Units?")
		return self.__IMMEUnitD
		
	def ReadImmedVals(self):
		"""
		Reads the immed Values and puts them into dict
		"""
		for n in self.__IMMESrcD:
			self.write("measurement:immed:Source "+str(self.__IMMESrcD[n])+";Type "+str(self.__IMMETypD[n]))
			self.__IMMEValD[n]=self.ask("measurement:immed:value?")
		return self.__IMMEValdD	
		
		
	def ReadUnit(self):
		"""
		Reads units for each channel and puts them in dict
		"""
		self.__unitD=dict.fromkeys(self.__Channels)
		for ch in self.__Channels:
			self.__unitD[ch]=self.ask("CH"+str(ch)+"?").split(";")[-1][1]#[-1] takes "V" from the List, [1] takes only the V
		return self.__unitD
		
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
			
	def Offset(self):
		"""
		Reads current Channel offsets
		"""
		self.__Offset=dict.fromkeys(self.__Channels)
		for n in self.__Channels:
			offset=self.ask("CH"+str(n)+"?")
			self.__Offset[n]=float(offset.split(";")[3])#gives Offset in divs
		
	def ReadInv(self):
		"""
		looks up if the channels are inverted
		"""
		self.__Inv=dict.fromkeys(self.__Channels)
		for n in self.__Channels:
			inv=self.ask("CH"+str(n)+"?").split(";")[-2]
			if inv== "ON":
				self.__Inv[n]=-1
			elif inv=="OFF":
				self.__Inv[n]=1
			else:
				raise TypeError("Da stimmt was net mit den Invs")
		return self.__Inv	
			
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
		return self.ask("Data:End?")
		
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
			val.append(float(self.__Inv[n])*(int(self.ask("Curve?"))+self.__Offset[n])/self.__widthD[self.__width]*5*self.__voltsDiv[n])
			#die self.__withD-Konstruktion ist nötig, um die übertragungsbreiten bei der Bestimmung
			#des Bereichs zu berücksichtigen
		return val
		
if __name__=="__main__":
	start_time=time.time()
	x=TDS2000bDriver(1689,869)#check
	setup_t=time.time()-start_time
	print("Das Setup dauert "+str(setup_t)+"s.\n")
	#print(x.ask("*IDN?"))#check
	print(x.__dict__)#check
	#x.SetChannels(1,2)#check
	#print("\n Read Inv: ",x.ReadInv(),"\n")
	#print(x.readChannels())#check	
	#print(x.ReadChanSingleValues())
	#print(x.ReadUnit())
		
	
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

Irgendwie schauen, dass man nicht aktive Kanäle (am Oszi) rauswirft, sonst
kann man die der Channellist hinzufügen und das Programm schmiert ab


"""
