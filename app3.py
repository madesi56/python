import sys
import os

sys.path.append('driver')    

from driver.gxnetClass import gxnet
from driver.gxnetFunction import *
from driver.clogger import clog
from driver.gxnetCommand import *


gx = gxnet()
c = clog(False)
cmd = gxnetCommand()
gx.OpenComm(1 , 1045)
#gx.sendOne(cmd.getTextList())

#gx.sendOne(cmd.restart())


#time.sleep(10)
while True:
    #
    gx.sendOne(cmd.getFirmwareRelease())
    #gx.sendOne(cmd.getTextList())
    print(quit)
    time.sleep(1)
    a = input("comando")
    if (a == 'z'):
        break

exit()

#while True:
    #gx.sendOne(cmd.getFirmwareRelease())
#    gx.sendOne(cmd.getTextList())
#    time.sleep(2)

