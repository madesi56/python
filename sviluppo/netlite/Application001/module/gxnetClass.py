import datetime
from operator import truediv
import socket
import sys
import time
from configparser import ConfigParser
from threading import Thread
from threading import Event
#from typing import Self
from module.gxnetFunction import *
import os
#import logging
from module.clogger import clog
from module.gxnetCommand import *
from module.gxnetErrors import *
from module.gxnetMenu import *


################################################
# classe gxnet 
# costruttore vuoto
################################################

# Metodi:
# OpenCom : apre la comunicazione verso il server
#           nel caso si vogliano recuperare i dati spontanei
# CloseComm : chiude la comunicazione verso il server (se era aperta)
#
# Funzioni interne alla classe
# LeggIni : legge i parametri di configurazioen per la 
#           comunicazione, i parametri TCP, le porte e il tipo di 
#           parametri da passare alla gx  

class gxnet():

   
    

    def __init__(self , _event):
        
        self.clog = clog()

        self.Client = socket.socket()
        self.Server = socket.socket()
        self.ServerAuto = socket.socket()
        
        self.clientstop = False
        self.serverstop = False
        self.serverSpstop = False
        
        self.event = Event()


        # variabile da usare per inviare i dati
        self.str2Send = []
        self.attesaConfermaMessaggio = False
       
        self.err = gxnetErrors()

        self.ev = _event
        #self.tev = MyThread(self.ev)
        #self.tev.start()

    def __str__(self):
        print("")
    
 
    #################################################################
    # metodi pubblici
    #################################################################
    
    def OpenComm(self, diz_config):
        
        self.DEVICE_PORT = int(diz_config["DEVICE_PORT"])
        self.DEVICE_TELEGRAM_TYPE = int(diz_config["DEVICE_TELEGRAM_TYPE"])
        self.DEVICE_PORT_AUTO = int(diz_config["DEVICE_PORT_AUTO"])
        self.DEVICE_IP = diz_config["DEVICE_IP"]
        self.DEVICE_SYNC= int(diz_config["DEVICE_SYNC"])
        self.DEVICE_CONVERSION= int(diz_config["DEVICE_CONVERSION"])
        self.SERVER_IP= diz_config["SERVER_IP"]
        self.DEVICE_PROFIBUS= diz_config["DEVICE_PROFIBUS"]
        
        self.clog.show("-".ljust(80,'-'))
        self.clog.show("crea il threading per il server ...")
        self.__ThreadServer()

        if (self.DEVICE_TELEGRAM_TYPE ==1):
            self.clog.show("-".ljust(80,'-'))
            self.clog.show("crea il threading per il serverSp ...")
            self.__ThreadAutoServer()
            #self.__createServer()
            #self.waiting_server()
            self.clog.show("-".ljust(80,'-'))
        self.clog.show("crea il threading per il client")
        self.__ThreadClient()
        
        self.clientThread.start()
        time.sleep(0.5)
        self.serverThread.start()
        time.sleep(0.5)
        self.serverThreadAuto.start()
        time.sleep(0.5)
        self.clog.show("Start terminated .....")
        self.clog.show("-".ljust(80,'-'))

        
        time.sleep(0.2)

   
    def CloseComm(self):
        self.clog.show("chiude i socket client e server ")

        #self.serverThread.join()

        #time.sleep(1)

        self.Server.close()
        self.ServerAuto.close()
        self.Client.close()
    

    
    ######################################################################
    # Start threading ...
    ######################################################################
    
    def __ThreadClient(self):
            
        #self.__connecting_client()
    
        threads = []
        self.clientThread = Thread(target=self.__waitingClient , args= (self.event,))
        #self.shutdown = threading.Thread(target=self.shutdown_client)
        threads.append(self.clientThread)
        
    def __ThreadServer(self):

        #self.__initServer()
        threads = []
        self.serverThread = Thread(target=self.__waiting_server, args= (self.event,))
        #self.shutdown = threading.Thread(target=self.shutdown_server)
        threads.append(self.serverThread)
    
    def __ThreadAutoServer(self):
        if (int(self.DEVICE_PORT) == 0):
            self.clog.show("porta = 0 ... no server " )
        else:
            #self.__initServerAuto()
            threads = []
            self.serverThreadAuto = Thread(target=self.__waiting_server_auto, args= (self.event,))
            #self.shutdown = threading.Thread(target=self.shutdown_server_sp)
            threads.append(self.serverThreadAuto)
         
    def __initServer(self):
        
        self.clog.show("Server create ...")
        # '192.168.1.133'
        HOST = self.SERVER_IP
        #  10045
        PORT = int(self.DEVICE_PORT)
        self.clog.show("Server information :  " + str(HOST) + " port: " + str(PORT) + "")
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Server.bind((HOST, PORT))
        self.clog.show("Server listening ")
        self.Server.listen()
            

    def __initServerAuto(self):

        self.clog.show("Server sp create ...")
        # '192.168.1.133'
        HOST = self.SERVER_IP
        #  10045
        PORT = int(self.DEVICE_PORT_AUTO) #int(self.hostPort)
        self.clog.show("Server information :  " + str(HOST) + " port: " + str(PORT) + "")
        self.ServerAuto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ServerAuto.bind((HOST, PORT))
        self.clog.show("ServerAuto listening ")
        self.ServerAuto.listen()
        
        
             
    def __waiting_server(self, event):

        self.clog.show("start server")
        
        self.__initServer()

        while (self.serverstop == False):
            if (event.is_set()):
                self.Server.close()
                break

            try:
                conn, addr =self.Server.accept()
            except Exception as ex:
                self.clog.show("Error server " + str(ex))
                break

            with conn:

                self.clog.show("-".ljust(80,'-'))
                self.clog.show('<-- Server : request connection accepted  by ... [' +  str(addr) + "]")
                while self.serverstop == False:
                    #print ("Server listeninig ... ")
                    try:
                        data = conn.recv(2048)
                    except ConnectionError as er:
                        self.clog.show("Errore connessione " + str(er))   
                    except Exception as er2:
                        self.clog.show("Errore generico " + str(er2))   
                    #self.clog.show("**********  CICLO SERVER *********")
                    if data != "":
                        if str(data).find("BIZERBA_TCP_INFO") > -1:
                            #for i in range(len(data)):
                            #    print (i , data[i]);
                            
                            self.clog.show("SRV_RX  <-- " + str(data))
                            #print("<-- " + data)
                            #ret = self.__convertFromScaleToAscii(data)
                            #print (ret)
                            self.clog.show("SRV_TX  --> " + "BIZERBA_OK")

                            conn.send(b'BIZERBA_OK')
                        else:
                            conn.send(b'BIZERBA_OK')
                            self.clog.show("SRV_RX  <-- " + data.decode())
                            ret = convertHex2Ascii(data.decode())

                            #ret =convertHex2Ascii(data)
                            self.clog.show("SRV_RX  <-- " + ret.replace('\n','@0A'))
                            time.sleep(0.01)
                            self.clog.show("SRV_TX  --> " + "BIZERBA_OK")
                            #self.__manageDataReceived(ret, conn)
                            risposta = self.__preparaRisposta(ret,conn)
                            if (risposta !=""):
                                #self.str2Send.append( risposta)
                                #self.clog.show("CLI --> " + risposta)

                                #risposta = convertAscii2Hex(risposta, self.gxProfibus)
                                #self.Client.send(risposta.encode())
                                #self.sendOne(risposta)
                                pass
                    #self.clog.show("")
                self.clog.show("-".ljust(80,'-'))
        else:
            self.clog.show("server terminato")


    def shutdown(self):
        self.event.set()
        self.clientThread.join()
        #self.serverThread.join()
        #self.serverThreadAuto.join()
        

    
    def __waiting_server_auto(self,event):

        self.clog.show("start waiting serverAuto")
        self.__initServerAuto()

        while True:
            if (event.is_set()):
                self.ServerAuto.close()
                break
            try:
                conn, addr =self.ServerAuto.accept()
            except Exception as ex:
                self.clog.show("Error serverS " + str(ex))
                break
            
            with conn:
                self.clog.show('<-- ServerAuto : Connected by ... [' +  str(addr) + "]")

                while True:
                    #print ("Server listeninig ... ")
                    data = conn.recv(2048)
                    #self.clog.show("**********  CICLO SERVER *********")
                    if data != "":
                        if str(data).find("BIZERBA_TCP_INFO") > -1:
                            #for i in range(len(data)):
                            #    print (i , data[i]);
                            

                            self.clog.show("AUT_RX  <-- " + str(data))
                            #print("<-- " + data)
                            #ret = self.__convertFromScaleToAscii(data)
                            #print (ret)
                            self.clog.show("AUT_TX  --> " + "BIZERBA_OK")

                            conn.send(b'BIZERBA_OK')
                        else:
                            conn.send(b'BIZERBA_OK')
                            ret = self.__convertFromScaleToAscii(data)
                            #ret = convertHex2Ascii(data.decode())
                            

                            #ret =convertHex2Ascii(data)
                            self.clog.show("AUT_RX  <-- " + ret.replace('\n','@0A'))
                            self.clog.show("AUT_TX  --> " + "BIZERBA_OK")
                            #self.__manageDataReceived(ret, conn)
                            risposta = self.__preparaRisposta(ret,conn)
                            if (risposta !=""):
                                self.sendOne(risposta)
                            self.ev.set(ret)
                            
                    #self.clog.show("")
        else:
            self.clog.show("serverSp terminato")


    def __convertFromScaleToAscii(self,strIn):
         
        b = bytes(strIn)
        numBytes = sys.getsizeof(b)
        convertedString=""
        try:
            for i in range (0,numBytes):
                dec = b[i]
                hexAscii = dec2Any(dec,16)
                convertedString += hexAscii
        except Exception as err:
                    pass
        ret =convertHex2Ascii(convertedString)
        return ret

    def __preparaRisposta( self,ret, conn):
       
        confirm=""
        self.invioConferma=True

        #self.attesaConfermaMessaggio =False

        if (ret[0:2] =="A!"):
            ret = ret.replace("A!","")
        try:

            token = ret.split("|")
            if (token[0] =="PL03"):
                decStatus = token[1]
                hexStatus =hex(int(decStatus))

                self.clog.show("PARSE   <-- " + str(hexStatus))

                return ""                
            if (token[0] == "WT65"):
                licenceCode = takeValueFromString(ret,"WT65")
                #licenceAnswer = self.adattaLicenza(licenceCode)
                #licenceAnswer = "EQP9255MEH7F6"
                return "" #("A!WT65|" + licenceAnswer.replace('\x00',''))
            if (token[0] =="PV04"):
                # writeDb(ret)
                self.clog.show("<-- " + "single package ")
                return ""                
        
            elif (token[0] =="PV01"):
                # writeDb(ret)
                handle = token[2]
                return("A!PW03|" + handle)
            elif (token[0] == "PV07"):
                # writeDb(ret)
                handle = token[5]
                return("A!PW10|" + handle + "|")
            elif (token[0] =="WV05"):
                self.__analisiDialoghi(ret)
                return ""
            elif (token[0] =="XV00"):
                return("A!LW00|" + token[0])
            elif (token[0] == "GL44"):
                lotto = token[1]
                return("A!LW00|" + token[0])
            elif (token[0] == "PL14"):
                self.clog.show("    " + "PSL_ALIVE_INFO")
                #self.str2Send.append("A?WT65|3")
                return ""
            elif (token[0] == "LV00" ):
                errNumber = takeValueFromString(ret, "LW01")
                self.clog.show("Error : " + self.err.getError(errNumber))
                return ""
            elif (token[0] == "DV05"):
                #confirm= "A!LW00|" + token[0]
                #self.str2Send.append(confirm)
                #self.invioConferma=False
                return ""
                pass
            elif (token[0] == "DW00"):
                #confirm= "A!LW00|" + token[0]
                #self.str2Send.append(confirm)
                self.clog.show("Fine ricezione ")
                #self.invioConferma=False
                return("A!LW00|" + token[0])
                #return ""
            else:
                #self.clog.show("--> " + "confirm data modified")
                return("A!LW00|" + token[0])
                #conn.send(strOut.encode())
        except Exception as err:
                self.clog.show("ERROR __PreparaRisposta --> " + str(err))
                return ""

    def __analisiDialoghi(self, ret):
        token = ret.split("|")
        tipoButton = takeValueFromString(ret,"WW07")
        if (tipoButton == '0'):
            self.clog.show("--> " + "button " + token[2] + " pushed")
        elif (tipoButton == '1'):
            self.clog.show("--> " + "button " + token[2] + " alfanumeric")
            textReceived = takeValueFromString(ret,"WT0A")
            self.clog.show("--> " + "received  " + textReceived)
        elif (tipoButton == '2'):
            self.clog.show("--> " + "button " + token[2] + " numeric")
            pluToSend = takeValueFromString(ret,"WL0A")
            self.clog.show("--> " + "received  " + pluToSend)
        else:
            self.clog.show("--> " + "button " + token[2] + " non gestito ")

    def adattaLicenza(self , licenceIn):
        for i in range(len(licenceIn)):
            n = ord(licenceIn[i])
            ret = self.rightRotate(n,2)

        
    
    def leftRotate(self , n, d):
        INT_BITS = 32
        # In n<<d, last d bits are 0.
        # To put first 3 bits of n at
        # last, do bitwise or of n<<d
        # with n >>(INT_BITS - d)
        return (n << d)|(n >> (INT_BITS - d))

    def rightRotate(self ,n, d):
        INT_BITS = 32
        # In n>>d, first d bits are 0.
        # To put last 3 bits of at
        # first, do bitwise or of n>>d
        # with n <<(INT_BITS - d)
        return (n >> d)|(n << (INT_BITS - d)) & 0xFFFFFFFF

    ##################################################################
    # CLIENT FUNCTION 
    #################################################################
    

    def __connecting_client(self):
            
        CLIENTIP = self.DEVICE_IP   #  192.168.1.250
        CLIENTPORT = int(self.DEVICE_PORT)  #  1045
        self.clog.show("ClientInfo : " + str(CLIENTIP) + " port: " + str(CLIENTPORT) +"")
        while True:
            try:
                self.Client.connect((CLIENTIP,CLIENTPORT))
                self.Client.settimeout(1)

                # client.settimeout(1)
                self.clog.show("Client connected")
                self.__infotelegram()
                return
            except Exception as err:
                self.clog.show("ERROR " + str(err))
                self.clog.show("connection failed waiting 2 seconds .. retry " )
                time.sleep(2)
    
    def __infotelegram(self):
        
        #print("ClientSync : " + str(self.clientSync ) + " Conversion : " + str(self.clientConversion))
        self.clog.show("Send info telegram porta " + str(self.DEVICE_PORT))
        
        port = int(self.DEVICE_PORT) #int(self.mnu.getFromIni("HOSTPORT"))
        hPort = int(port/256)
        lPort = port - 256 * hPort

        # 10045 27 3D --> 39 61
        # 1045 04 15 --> 04 21
        msg= 'BIZERBA_TCP_INFO'
        msg += chr(hPort)
        msg += chr(lPort)
        msg += chr(1)
        msg += chr(0)
        msg += chr(self.DEVICE_SYNC)
        msg += chr(self.DEVICE_CONVERSION)
        msg += chr(35)
        msg += chr(64)
        #for i in range(len(msg)):
        #    print (i , msg[i])
        
        self.clog.show("--> " + str(msg.encode()))
        try:
            # print(msg)
            # print(msg.encode())
            #print("ClientiSync : " + str(self.clientSync) + ".\n")
            self.clog.show("CLI_TX  --> " + msg)
            self.Client.send(msg.encode())
            if (self.DEVICE_SYNC==1):
                #print("wait sync ... ")
                response=self.Client.recv(1024)
                self.clog.show("CLI_RX  <-- " + response.decode())
                
        except Exception as e:
            self.clog.show("ERROR " + str(e))
   
    def sendOne(self, strtoSend):
        if (strtoSend != ""):
            self.str2Send.append(strtoSend)
            self.invioConferma =False
            while True:
                time.sleep(0.1)
                if (len(self.str2Send) == 0):
                    break;     
    
    
    def __waitingClient(self, event):

        #self.clog.show("" + "client connection ")
        self.__connecting_client()
        #self.clog.show("" + "success ")
        self.erroreConnessione=False
        terminate = False
        while terminate==False:
            time.sleep(0.2)
            if (event.is_set()):
                self.Client.close()
                
                terminate=True
            else:
                try:
                    #print ( "client waiting ...")
                    if (len(self.str2Send) > 0):
                        command = self.str2Send[0]
                        if (command != ""):
                            ###################################################
                            # invio dato 
                            ###################################################
                            # tolgo il comando dalla lista .... pop
                            #self.str2Send.pop(0)
                            # invio dati in HEX-ASCII
                            if (self.DEVICE_CONVERSION ==1):   

                                strHex = convertAscii2Hex(command, self.DEVICE_PROFIBUS)
                                
                                self.clog.show("CLI_TX  --> " + strHex)
                                self.clog.show("CLI_TX  --> " + command)
                                try:
                                    self.Client.send(strHex.encode())
                                except Exception as e :
                                    self.clog.show("errore client " + str(e))

                            #while True:
                            #time.sleep(0.2)

                            #while True:
                            try:
                                response= self.Client.recv(2048).decode()
                            except socket.timeout as e:
                                print ('')
                                response=''
                                break
                            except Exception as er:
                                self.clog.show("ERROR " + str(er))
                                self.erroreConnessione=True
                                break
                            self.clog.show("CLI_RX  <-- " + response) 
                            if int(self.DEVICE_PORT) == 0:
                                if response != "":
                                    self.clog.show("CLI_RX-1  <-- " + response) 
                                    #if (response.find("BIZERBA_OK")) > -1:
                            
                                    response = response.replace("BIZERBA_OK",'')
                                    self.clog.show("CLI_RX-2  <-- " + response) 
                                    if (response) !='':
                                        asciiResponse = convertHex2Ascii(response)
                                        self.clog.show("CLI_RX   <-- " + asciiResponse) 
                                        self.clog.show("CLI_TX   --> " + 'BIZERBA_OK')
                                        self.Client.send('BIZERBA_OK'.encode())

                                        #if (response.find("DW01")) == -1:
                                        #    break
                                        #if (response.find("DW00"))== 0:
                                        #    break
                                        #if (response.find("DW01"))>0:
                                        #    pass
                                        #response=''
                            self.str2Send.pop(0)
                except Exception as er1:
                        self.clog.show("ERRORE !!!  --> " + str(er1))
            
                if (self.erroreConnessione):
                    self.Client.close()
                    self.Client = socket.socket()
                    self.__connecting_client()

            #self.clog.show("client terminato ")
            
  
    def __parseError(self, strRx):
        if (takePositionFromString(strRx,"LW01") >0):
            errNumber = takeValueFromString(strRx, "LW01")
            self.clog.show("Error : " + self.err.getError(errNumber))
    
    def __parseMemoryCard(self , strRx):
        if (takePositionFromString(strRx,"MV08") >0):
            self.clog.show("Risposta MEMORY CARD")
            self.clog.show(strRx)
            self.splitSinglePackage(strRx)

    def clientSend(self , _str2Send):
        #self.clog.show("--> " + _str2Send)
        self.Client.send(b'" + _str2Send + "')

    def splitSinglePackage(self, str2Split):
    
        str2Split = str2Split.replace ("|PV04", "#PV04")
        x = str2Split.split("#")
        for row in range(len(x)):
            self.clog.show(x[row])
        

         



        
    

  
    
    
   