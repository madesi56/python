import os
import sys

sys.path.append('driver')    

from driver.gxnetClass import gxnet
from driver.gxnetFunction import *
from driver.clogger import clog
from driver.gxnetCommand import *
from driver.gxnetMenu import *
from driver.gxnetPlu import *
from driver.gxnetEvents import *

from datetime import datetime
import time


def main() -> int:

    c = clog()
    c.show("****************************************************")
    c.show("START NEW APPLICATION " +  getDateTime())
    c.show("****************************************************")

    ev = MyEvent()
    tev = dataArrived(ev, c)
    tev.start()

    #  Classi usate
    mnu = menu()
    gx = gxnet(ev)  

    c.show("Clear screen")
    mnu.clearScreen()

   
    c.show("OpenPort spData=yes port=1046" )
    gx.OpenComm(1 , 1046)


    try:
        while True:
        
            comando = input("Choose a command --> ??? \n")
            if (comando == 'z'):
                gx.CloseComm()
                break
            elif (comando == "m"):
                mnu.clearScreen()
                mnu.showCommand()
            else:
                print(mnu.runCommand(comando, gx))
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
            d=[]
            while 1:
                event_type = self.event_handler.wait()
                self.event_handler.clear()
                if (event_type != "0"):
                    d = parseGxNetString(event_type)
                    for i in range(len(d)):
                        self.c.show(d[i])
                    
                    self.c.show(takeValueFromString( event_type, 'GT90'))

if __name__ == '__main__':
    main()
    try:
        sys.exit(0)
    except Exception as e:
        pass