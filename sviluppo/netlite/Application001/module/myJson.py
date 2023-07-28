import os
import json



class myJson():

    def __init__(self , filename ):
        self.filename = filename

    def firstRecord(self ,d1):
        with open(self.filename , "w") as fp:
            json.dump(d1,fp,indent=6)     

    def addRecord(self , d2 ):
        try:
            l = []

            with open(self.filename , "r") as fp:
                d1 =json.load(fp)

                d3 = {**d1, **d2}

            with open(self.filename , "w") as fp:
                json.dump(d3,fp, indent=6)

        except Exception as e:
            print (str(e))







