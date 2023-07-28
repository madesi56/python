import json
import os

class gxnetPlu():
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        pass

    def getPluFromJsonFile(self):
        pcname = os.getenv("COMPUTERNAME")
        actualPwd = os.getcwd()
        pluFile = actualPwd  + "/config/" + "plu.json"
        

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
        pluFile = actualPwd  + "/config/" + "rana.json"
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
