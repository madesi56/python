import sys
import os

sys.path.append('driver')    

from driver.gxnetClass import gxnet
from driver.gxnetFunction import *
from driver.clogger import clog
from driver.gxnetCommand import *



gx = gxnet()
c = clog()
cmd = gxnetCommand()

gx.OpenComm(0 , 1046)
while True:
    gx.sendOne(cmd.getLicense(1))
    time.sleep(2)

