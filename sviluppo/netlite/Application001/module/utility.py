
from configparser import ConfigParser
import os
import time

class utility():

    def leggiIni(self): 

            #crea una sequenza di stringhe
            config = ('DEVICE_PORT_AUTO',
                      'DEVICE_PORT', 
                      'DEVICE_IP',
                      "DEVICE_TELEGRAM_TYPE",
                      "DEVICE_NAME",
                      "DEVICE_NUMBER",
                      "DEVICE_PROFIBUS",
                      "DEVICE_CHANNEL",
                      "DEVICE_SYNC",
                      "DEVICE_CONVERSION",
                      "SERVER_IP")

            #crea il dizionario, `dizionario_esempio`, usando il metodo fromkeys()
            diz_config = dict.fromkeys(config)

            #print(diz_config)

            parser=ConfigParser ()
            actualPwd = os.getcwd()
            fileIni = actualPwd  + "/config" # +  ""+ str(pcname) 
            fileIni += "/" + "app.ini"
            parser.read( fileIni)

            try:

                diz_config["DEVICE_IP"] = parser.get('DEFAULT','DEVICE_IP', fallback = '192.168.68.200')
                diz_config["DEVICE_NUMBER"] = parser.get('DEFAULT','DEVICE_NUMBER' , fallback=1)
                diz_config["DEVICE_PROFIBUS"] = parser.get('DEFAULT','DEVICE_PROFIBUS', fallback = 2)
                diz_config["DEVICE_CHANNEL"] = parser.get('DEFAULT','DEVICE_CHANNEL', fallback='E')
                diz_config["DEVICE_PORT"] = parser.get('DEFAULT','DEVICE_PORT', fallback=1045)
                diz_config["DEVICE_PORT_AUTO"] = parser.get('DEFAULT','DEVICE_PORT_AUTO',fallback=10045)
                diz_config["DEVICE_TELEGRAM_TYPE"] = parser.get('DEFAULT','DEVICE_TELEGRAM_TYPE', fallback = 1)
                diz_config["DEVICE_NAME"] = parser.get('DEFAULT','DEVICE_NAME', fallback='MY GLP NUMBER ONE')
                diz_config["DEVICE_SYNC"] = parser.get('DEFAULT','DEVICE_SYNC', fallback=1)
                diz_config["DEVICE_CONVERSION"] = parser.get('DEFAULT','DEVICE_CONVERSION', fallback=1)
                diz_config["SERVER_IP"] = parser.get('DEFAULT','SERVER_IP', fallback="0.0.0.0")
            
                return diz_config
            
            except Exception as e:
                self.clog.show("ERROR " + str(e))    
                return 
            
   