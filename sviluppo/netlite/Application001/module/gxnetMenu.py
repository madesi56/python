import os
from configparser import ConfigParser

from module.clogger import *
from module.gxnetCommand import *
from module.gxnetClass import *
#from module.gxnetPlu import *


class menu():

    def __init__(self) -> None:
        self.comandi = self.__readCommand()
        self.dComand=''
        pass

    def showCommand(self):
        
        for i in range(0, len(self.comandi)):
            s = '-'
            #print (s.ljust(80 , "-"))
            print ("{:<30}  ".format(self.comandi[i]))
            #if (i%10 == 0 and i>0):
            #    input("press for next ...")

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def getFromIni(self, chiave):

        parser=ConfigParser ()
        pcname = os.getenv("COMPUTERNAME")
        actualPwd = os.getcwd()

        fileIni = actualPwd  + "/config" # +  ""+ str(pcname) 
        fileIni += "/" + "app.ini"
        parser.read( fileIni)

        try:
            value = parser.get('DEFAULT',chiave)
            return value        
        except Exception as e:
            return ""
            #clog.show("ERROR " + str(e))   

    def runCommand(self , comando, gx):
        
        comando=int(comando)
        cmd = gxnetCommand()
        #plu = gxnetPlu()
        #gx = gxnet()
        result =""
        
        if (comando == 1):
            gx.sendOne(cmd.getPing())
        elif (comando== 2):
            gx.sendOne(cmd.getFirmwareRelease())
        elif (comando== 3):
            gx.sendOne(cmd.getLicense(1))
        elif (comando== 4):
            gx.sendOne(cmd.sendText(input("text number ? "), input("text value ? ")))
        elif (comando== 5):
            gx.sendOne(cmd.setData2Scale())
        elif (comando== 6):
            gx.sendOne(cmd.setTime2Scale())
        elif (comando== 7):
            gx.sendOne(cmd.createError())
        elif (comando==8):
            gx.sendOne(cmd.changePlu("PluNumber ?"))
        elif (comando==9):
            gx.sendOne(cmd.enableChannel(input("Channel [A-F] ? ")))
        elif (comando==10):
            gx.sendOne(cmd.disableChannel(input("Channel [A-F] ? ")))
        elif (comando==11):
            gx.sendOne((input("Comando gxnet ...")))
        elif (comando == 12):
            gx.sendOne(cmd.setPushButton(1, "Push me "))
        elif (comando == 13):
            gx.sendOne(cmd.setNumericalButton(input("Button Number [1-16]"), input("Button text")))
        elif (comando == 14):
            gx.sendOne(cmd.setAlphaButton(input("Button Number [1-16]"), input("Button text")))
        elif (comando ==15) :
            pluData= cmd.getPluFromJsonFile()
            for i in range(len(pluData)):
                gx.sendOne (pluData[i])
        elif (comando ==16) :
            gx.sendOne (cmd.getMemoCard())
        elif (comando == 17):
            gx.sendOne (cmd.deleteAllPluTable())
        elif (comando == 18):
            pluNumber= input("Plu da cancellare ?? --- > ")
            gx.sendOne (cmd.deletePlu(pluNumber))
        elif (comando == 19):
            pluNumber= input("Plu da inviare ?? --- > ")
            str2Send= cmd.ranaChangePlu(pluNumber)
            if (str2Send ==""):
                gx.sendOne(cmd.sendMessage("ATTENZIONE PLU NON ESISTE"))
            else:
                gx.sendOne (str2Send)
        elif (comando== 20):
            gx.sendOne (cmd.channelList())
        elif (comando == 21):
            gx.sendOne (cmd.getPluList())
        elif (comando == 22):
            gx.sendOne(cmd.getTextList())
        elif (comando == 23):
            gx.sendOne(cmd.macchinaManuale())
        elif (comando == 24):
            gx.sendOne(cmd.macchinaAutomatico())   
        elif (comando == 25):
            gx.sendOne(cmd.getProfibus())   
        elif (comando == 26):
            profibusNumber= input("Profibus number ?? --- > ")
            gx.sendOne(cmd.setProfibus(profibusNumber))
        elif (comando == 27):
            gx.sendOne(cmd.getMachineNumber())
        elif (comando == 28):
            machineNumber= input("Machine number ?? --- > ")
            gx.sendOne(cmd.setMachineNumber(machineNumber))
        elif (comando == 29):
            gx.sendOne(cmd.getCodeStrctureList())
        elif (comando == 30):
            gx.sendOne(cmd.getAutoParameterList())
        elif (comando == 31):
            gx.sendOne(cmd.getEtiParameterList())
        elif (comando == 98):
            gx.sendOne(cmd.printSum1())
        elif (comando == 97):
            gx.sendOne(cmd.printSum2())
        elif (comando == 96):
            gx.sendOne(cmd.printSum3())
        elif (comando == 99):
            gx.sendOne(cmd.printLabel())
        elif (comando == 100):
            gx.sendOne(cmd.reset())
        elif (comando == 101):
            gx.sendOne(cmd.restart())

        else:
            result = "Comando non supportato ..."
        return result

    def __readCommand(self):
        _comandi = []
        _comandi.append('1 ping')
        _comandi.append('2 firmware')
        _comandi.append('3 license')
        _comandi.append('4 text')
        _comandi.append('5 data')
        _comandi.append('6 ora')
        _comandi.append('7 errore')
        _comandi.append('8 cambio plu')
        _comandi.append('9 enable channel')
        _comandi.append('10 disable channel')
        _comandi.append('11 gxnet direct')
        _comandi.append('12 imposta pushButton')
        _comandi.append('13 imposta numericButton')
        _comandi.append('14 imposta alphaButton')
        _comandi.append('15 send plu to scale')
        _comandi.append('16 getMemo card')
        _comandi.append('17 delete all plu')
        _comandi.append('18 delete from plu to plu')
        _comandi.append('19 cambio plu rana ')
        _comandi.append('20 getChannel list')
        _comandi.append('21 getPlu list')
        _comandi.append('22 getText list')
        _comandi.append('23 macchina Manuale')
        _comandi.append('24 macchina Automatico')
        _comandi.append('25 getProfibus')
        _comandi.append('26 setProfibus')
        _comandi.append('27 getMachineNumber')
        _comandi.append('28 setMachineNumber')
        _comandi.append('29 getBarcodeStruct list')
        _comandi.append('30 getAutoParam list')

        _comandi.append('96 print sum3')
        _comandi.append('97 print sum2')
        _comandi.append('98 print sum1')

        _comandi.append('99 print single label')
        _comandi.append('100 reset')
        _comandi.append('101 restart')
        

        return _comandi