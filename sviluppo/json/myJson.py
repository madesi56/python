import os
import json



class myJson():

    def __init__(self , filename , d1):
        self.filename = filename
        with open(filename , "w") as fp:
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


def main():
    pass
    d1 = {"01" : {"PV04":"","PW02" : "11", "PD04" : "KG;-3;110"}}
    d2 = {"02" : {"PV04":"","PW02" : "12", "PD04" : "KG;-3;120"}}
    d3 = {"03" : {"PV04":"","PW02" : "13", "PD04" : "KG;-3;130"}}
    d4 = {"04" : {"PV04":"","PW02" : "14", "PD04" : "KG;-3;140"}}
    d5 = {"05" : {"PV04":"","PW02" : "15", "PD04" : "KG;-3;150"}}
    filename="prova.json"
    j = myJson(filename, d1 )
    j.addRecord(d2)
    j.addRecord(d3)
    j.addRecord(d4)
    j.addRecord(d5)
    




main()






