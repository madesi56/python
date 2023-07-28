import string
import logging
from datetime import datetime
import time
import os
import sys

class clog():

    def __init__(self):
        #self.message = message
        current_date = datetime.now()
        
        strdate = str(current_date.year).zfill(4) + str(current_date.month).zfill(2) + str(current_date.day).zfill(2)
        actualPwd = os.getcwd()
        
       
        pathLog = actualPwd  + "/log/"
        self.logname= pathLog + "log_" + strdate + ".log"
        self.noShowBizerbaOk = False

        #self.show()


    def show(self , message):
        __fileName = self.logname
        logging.basicConfig(filename=__fileName,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
        print (message)
        logging.info(message)

        #if (self.noShowBizerbaOk == True):
        #    if (message.find("BIZERBA_OK")>-1):
        #        pass
        #    else:
        #        print (message)
        #else:
        #    print (message)

        #logging.info(message)

#logger = logging.getLogger('urbanGUI')