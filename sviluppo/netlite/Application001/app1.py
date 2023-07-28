
import sys
import os
import os.path

sys.path.append('module')    

from module.gxnetClass import gxnet
from module.gxnetFunction import *
from module.clogger import clog
from module.gxnetCommand import *
from module.gxnetMenu import *
from module.gxnetPlu import *
from module.gxnetEvents import *
from module.utility import *
from module.myJson import myJson

from datetime import datetime
import time


def main() -> int:

    
    #print (sys.path)
   
    mnu = menu()
    mnu.clearScreen()

    c = clog()
    c.show("Clear screen")
    c.show("****************************************************")
    c.show("START NEW APPLICATION " +  getDateTime())
    c.show("application path : " + os.getcwd())
    c.show("****************************************************")

    ev = MyEvent()
    tev = dataArrived(ev, c)
    tev.start()


    #  Classi usate
    uti = utility()
    mnu = menu()
    gx = gxnet(ev)
    
    cmd = gxnetCommand()

    
    
    device_config = uti.leggiIni()

    for key in device_config:
        c.show(key + ": " + str(device_config[key]))

    gx.OpenComm(device_config)

    initStr = "A!LV01|" 
    initStr += cmd.getGxChannel(str(device_config["DEVICE_CHANNEL"])) + "|" + "1" + "|"
    initStr += "GL14|" + str(device_config["DEVICE_NUMBER"]) + "|"
    initStr += "WT64|" + str(device_config["DEVICE_NAME"]).replace('\n','@0A') + "|"
    initStr += "LX02"
            
    
    gx.sendOne(initStr)

    time.sleep(1.0)

    try:
        while True:
        
            comando = input("Digit command ? ---> ")
            if (comando == 'z'):
                gx.shutdown()
                break
            elif (comando == "m"):
                mnu.clearScreen()
                mnu.showCommand()
            elif ( comando.isdigit() ):
                print ("waiting command execution ... ")
                print(mnu.runCommand(comando, gx))
            else:
                print ("command not allowed ... ")

            time.sleep(1)        

    except KeyboardInterrupt as e:
        # quit
        print (str(e))
        sys.exit()

    return 0


def getDateTime():
    current_date = datetime.now()
    strdate = str(current_date.day).zfill(2) + "-" + str(current_date.month).zfill(2) + "-" + str(current_date.year).zfill(4)
    strdate += " " + str(current_date.hour).zfill(2) + str(current_date.minute).zfill(2) + str(current_date.second).zfill(2)
    return strdate

class dataArrived(Thread):
        def __init__(self, event_handler , _clog):
            self.c=_clog
            Thread.__init__(self)
            self.event_handler = event_handler

        def run(self):
            d={}
                 
            while 1:
                event_type = self.event_handler.wait()
                self.event_handler.clear()
                if (event_type != "0"):
                    d = parseGxNetString2Dict(event_type)
                    print (type(d))
                    print (d)
                   

                    filename=""
                    if ( "PV04" in d):
                        filename="singlePackage.json"
                    elif ("PV01" in d):
                        filename="totalPackage.json"
                    else:
                        return

                    gl16 = takeValueFromString( event_type, 'GL16')
                    d1 = {gl16 : d}

                    j = myJson(filename)

                    path = "./" + filename
                    if (os.path.isfile(path)):
                        j.addRecord(d1)
                    else:
                        j.firstRecord(d1)                        
                    #if (os.path.isfile(path)):
                    #    fp = open(filename, 'a') 
                    #    dex = json.load(fp)
                    #    fp.close()

                    #    fp = open(filename, 'w') 
                    #    dex.append(dact)
                    #    json.dump(dex,fp,indent=6)
                    #else:
                    #    fp = open(filename, 'a') 
                    #    fp = open(filename, 'w') 
                    #    dex.append(dact)
                    #    json.dump(dex,fp,indent=6)

                            


                    #    with open(filename, 'a') as fp:
                            
                    #jsonString = json.dump(d,)
                    #with open(filename, 'a') as fp:
                    #     fp.write (jsonString)

                    #for i in range(len(d)):
                    #    self.c.show(d[i])
                    
                    #self.c.show(takeValueFromString( event_type, 'GT90'))

if __name__ == '__main__':
    main()
  