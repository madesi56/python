import datetime
import sys
import time
from configparser import ConfigParser
import os
#import logging
#from dll.clogger import clog



class gxnetErrors():

    def __init__(self):
        
        self.errori = {"1" : "Internal error" ,
          "2" : "Access denied",
          "3" : "Conversion refused" ,
          "4" : "Third-party command",
          "5" : "Data format error",
          "6" : "Value undershot",
          "7" : "Value exceeded",
          "8" : "Warning: Unit changed",
          "9" : "Error: set unit does not match device configuration (scale typ error)",
          "10" : "Warning: Standardization changed",
          "11" : "Reserved IW",
          "12" : "Reserved IW",
          "13" : "Not enough memory",
          "150" : "Labeling disabled",
          "151" : "Incorrect mode level",
          "152" : "Previous internal label not ready",
          "153" : "Total reached",
          "154" : " Previous label was not acknowledged by downstream printer",
          "155" : " Conditional printing was not executed",
          "156" : "The queue for remote print orders is not empty",
          "251" : " Scale function may not be executed because automatic machine is running",
          "850" :"General scale error during calibration commands",
          "851" :" Scale not connected or scale type error during calibration commands",
          "852" :"Scale not stationary during gross weight request",
          "853" :" Scale outside range during reset or gross weight request",
          "1000" :"Error switching on PLU",
          "1001" :"forwarded error from a downstream device via 'Send change'",
          "1250" :"Cancellation could not be executed",
          "2002" :"Code editor access denied",
          "2050" :"Code structure data error",
          "2151" :"Internal error",
          "2152" :"No access to memory card",
          "2154" :"Communication error",
          "2155" :"Memory card is full",
          "2156" :"Warning: Memory card almost full (from 1kByte free space)",
          "2250" :"Connection lost",
          "2251" :"Timeout - remote currently occupied",
          "2252" :"Bridge has not made a connection",
          "2253" :"Bridge transmission error",
          "2254" :"Bridge overloaded",
          "2255" :"Response is missing",
          "2256" :"Count incorrect, e.g. odd",
          "2350" :"Incorrect data index or addressing",
          "2450" :"No statistics data available",
          "2451" :"Interpreter is occupied",
          "2252" :"Setup was not completely saved",
          "2650" :"Data record not available",
          "2651" :"Data record cannot be deleted",
          "2652" :"Database key attribute incorrect",
          "2653" :"Database attribute incorrect",
          "2654" :"Incorrect database command parameter",
          "2655" :"Database error in dimension related values",
          "2656" :"Dimension related attributes have been converted",
          "2657" :"An unknown attribute has been used in a table",
          "2658" :"Device has to be switched off/on prior to command.",
          }
     
    def __str__(self):
        print (self.errori)

    def getError ( self ,errNumber):
        if errNumber in self.errori.keys():
            return self.errori[errNumber]
        else:
            return "sorry error not found !!!"
    
