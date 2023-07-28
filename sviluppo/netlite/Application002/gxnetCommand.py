from datetime import datetime
import json
import os
import sys

#sys.path.append('dll')    


class gxnetCommand():

    def __init__(self):
        pass

    def restart(self):
        return "A!XX0A|1"  

    def reset(self):
        return "A!XW15|0"  

    def setProfibus(self,profibusNumber):
        return "A!SL80|" + profibusNumber

    def getProfibus(self):
        return "A?SL80|0"

    def getPing (self):
        return "A?PL03|0"

    def getFirmwareRelease(self):
        return "A?WT0C|0"

    def getLicense(self , licNumber):
        return "A?WT65|" + str(licNumber)

    def getMachineNumber(self):
        return "A?GL14|0"

    def setMachineNumber(self,machineNumber):
        return "A!GL14|" + machineNumber

    def setMachineName(self,machineName):
        return "A!WT64|" + machineName

    def createError(self):
        current_date = datetime.now()
        strTime = str(current_date.hour).zfill(2) + str(current_date.minute).zfill(2) 
        strTime = "A!GL2B|" + strTime
        return strTime

    def setData2Scale(self):
        
        current_date = datetime.now()
        strdate = str(current_date.day).zfill(2) +  str(current_date.month).zfill(2) +  str(current_date.year).zfill(2)
        strdate = "A!GL2B|" + strdate
        return strdate

    def setTime2Scale(self):
        
        current_date = datetime.now()
        strTime = str(current_date.hour).zfill(2) + str(current_date.minute).zfill(2) 
        strTime = "A!GL2C|" + strTime
        return strTime

    def getData(self):
        
        current_date = datetime.now()
        strdate = str(current_date.day).zfill(2) + "-" + str(current_date.month).zfill(2) + "-" + str(current_date.year).zfill(4)
        return strdate

    def getTime(self):
        
        current_date = datetime.now()
        strdate = str(current_date.hour).zfill(2) + str(current_date.minute).zfill(2) + str(current_date.second).zfill(2)
        return strdate

    def sendText(self,textNumber, message):

        strToSend = "A!GT0" + str(textNumber) + "|" + message + "  " + str(datetime.now())
        return strToSend

    def changePlu(self,pluNumber):
        strToSend= "A!XV00|GL19|" + str(pluNumber)
        return strToSend

    def getGxChannel(self, channelName):
        if (channelName =="A"):
            strToSend= "GWBF"
        elif (channelName =="B"):
            strToSend= "GWC0"
        elif (channelName =="C"):
            strToSend= "GWC1"
        elif (channelName =="D"):
            strToSend= "GWC2"
        elif (channelName =="E"):
            strToSend= "GWC3"
        else:
            strToSend=""    
        return strToSend

    def enableChannel(self,channelName):
        if (channelName =="A"):
            strToSend= "A!GWBF|1"
        elif (channelName =="B"):
            strToSend= "A!GWC0|1"
        elif (channelName =="C"):
            strToSend= "A!GWC1|1"
        elif (channelName =="D"):
            strToSend= "A!GWC2|1"
        elif (channelName =="E"):
            strToSend= "A!GWC3|1"
        else:
            strToSend=""    
        return strToSend

    def disableChannel(self,channelName):
        if (channelName =="A"):
            strToSend= "A!GWBF|0"
        elif (channelName =="B"):
            strToSend= "A!GWC0|0"
        elif (channelName =="C"):
            strToSend= "A!GWC1|0"
        elif (channelName =="D"):
            strToSend= "A!GWC2|0"
        elif (channelName =="E"):
            strToSend= "A!GWC3|0"
        else:
            strToSend=""    
        return strToSend

    def setPushButton(self,buttonNumber, buttonText):
        strToSend= "A!WV04|WW06|" + buttonNumber + "|WW07|0|WW08|1|WT00|" +  buttonText + "|LX02"
        return strToSend

    def setNumericalButton(self,buttonNumber, buttonText):
        strToSend = "A!WV04|WW06|" + buttonNumber + "|WW07|2|WW08|1|WT00|" + buttonText + "|WL0A|0|WW09|9|LX02"
        return strToSend

    def setAlphaButton(self,buttonNumber, buttonText):
        strToSend = "A!WV04|WW06|" + buttonNumber + "|WW07|1|WW08|1|WT00|" + buttonText + "|WT0A| |WW09|12|LX02"
        return strToSend
   

    def getMemoCard(self):

        str2Send = "A?MW06|3000"
        return str2Send

    def deleteAllPluTable(self):
        str2Send = "A!DV06|DW01|0|LX02"
        return str2Send

    def deletePlu(self,pluNumber ):

        str2Send = "A!DV06|DW01|0|DX00|GL19|" + pluNumber + "|LX02"
        return str2Send

    def getPluList(self):
        str2Send = "A?DV05|DW01|0|LX02"
        return str2Send

    def getTextList(self):
        str2Send = "A?DV05|DW01|1|LX02"
        return str2Send

    def getAutoParameterList(self):
        str2Send = "A?DV05|DW01|4|LX02"
        return str2Send

    def getCodeStrctureList(self):
        str2Send = "A?DV05|DW01|6|LX02"
        return str2Send
    
    def getEtiParameterList(self):
        str2Send = "A?DV05|DW01|2|LX02"
        return str2Send


    def macchinaManuale(self):
        str2Send = "A!LV01|GW15|1|GW09|2|GD01|KG;-3;123|GWBA|0|XW06|128|LX02"
        return str2Send

    def macchinaAutomatico(self):
        str2Send = "A!LV01|GW15|3|GW09|0|GD01|KG;-3;0|GWBA|1|XW06|128|LX02"
        return str2Send

    def channelList(self):
        str2Send = "A?LV01|GWBF|0|GWC0|0|GWC1|0|GWC2|0|GWC3|0|LX02"
        return str2Send

    def sendMessage(self,message):
    
        message='PLU is not available?'
        #str2Send = "A!WV60|WW60|80|WW61|8|WT60|"+ message + "|WV62|LX02|LX02"
        str2Send = "A!WV60|WW60|80|WW61|8|WT60|"+ message + "|LX02"
        return str2Send

    def printLabel(self):
        str2Send = "A!LV01|XW06|128|XW0C|0|LX02"
        return str2Send

    def printSum1(self):
        str2Send = "A!LV01|XW06|128|XW0C|1|LX02"
        return str2Send
    def printSum2(self):
        str2Send = "A!LV01|XW06|128|XW0C|2|LX02"
        return str2Send
    def printSum3(self):
        str2Send = "A!LV01|XW06|128|XW0C|10|LX02"
        return str2Send
    
    def getPluFromJsonFile(self):
        pcname = os.getenv("COMPUTERNAME")
        actualPwd = os.getcwd()
        pluFile = actualPwd  + "/pluData/" + "plu.json"
        

        f = open(pluFile)
        data = json.load(f)

        #for i in data['plu_details']:
        #    print(i)

        toSend = []
        i =0
        for field in data["plu_details"]:
        
                       
            header = "A!DV05|DW01|0|"
            str2Send= header
            str2Send += "GL19|" + field["plu_id"] + "|" 
            str2Send += "GT90|" + field["plu_text"] + "|" 
            str2Send += "GL20|" + field["plu_id"] + "|" 
            str2Send += "GD01|" + "KG;-3;" + field["plu_nominalWeight"] + "|" 
            str2Send += "GD02|" + "KG;-3;" + field["plu_tare"] + "|" 
            str2Send += "GW09|" + field["type_eti"] + "|" 
            str2Send += "GD10|" + "EUR;-2;" + field["un_price"] + "|" 
            
            str2Send += "LX02"
            
            toSend.append(str2Send)
            #self.clog.show()
            #self.send2Client(str2Send)
            
            header = "A!DV05|DW01|1|"
            str2Send= header
            str2Send += "GL2F|" + field["plu_id"] + "|" 
            str2Send += "GT00|" + field["plu_text"] + "|" 
            str2Send += "LX02"
            #self.send2Client(str2Send)
            toSend.append(str2Send)

        return toSend
    

    def ranaChangePlu(self, pluNumber):
        pcname = os.getenv("COMPUTERNAME")
        actualPwd = os.getcwd()
        pluFile = actualPwd  + "/pluData/" + "rana.json"
        f = open(pluFile)
        data = json.load(f)

        toSend = []
        i =0

        str2Send=""
        for field in data["set_details"]:
            if (field["plu_id"] == pluNumber):
                str2Send= "A!LV01|"
                str2Send += "XW05|" + "1" + "|" # blocco etichettatura
                str2Send += "XV00|GL19|" + field["plu_id"] + "|LX02|" # cambio plu 
                str2Send += "GT61|" + field["plu_id"].zfill(8) + "|" # plu nel gt61
                str2Send += "GT90|" + field["plu_text"] + "|" # testo articolo
                str2Send += "GT63|" + field["lot_number"] + "|" # gt63 ??
                #str2Send += "GD02|" + "KG;-3;16" + "|" # tara
                str2Send += "GD01|" + "KG;-3;" + field["plu_nominalWeight"] + "|" # peso nominale
                #str2Send += "AL09|" + field["belt_speed"] + "|" 
                #str2Send += "ALE3|" + field["pack_lenght"] + "|" 
                #str2Send += "ALE4|" + field["pack_lenght_tolerance"] + "|" 
                #str2Send += "WW10|" + field["stat_flag"] + "|" 
                #str2Send += "AL01|" + field["light_distance"] + "|"
                #str2Send += "WL30|" + field["lower_limit"] + "|" 
                #str2Send += "WL31|" + field["upper_limit"] + "|" 
                #str2Send += "GLDB|" + field["metal_detector"] + "|"
                str2Send += "XW06|128|"
                str2Send += "LX02"

        return str2Send
