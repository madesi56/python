
import string


def convertiAsciiToNoConversion(strIn,):
        car=""
        strOut=""
        intcar=0
        for i in range(0,len(strIn),2):
            car=string[i:i+2]
            intcar=int(car,16)
            #intcar2 =chr(int(any2Dec(car,16)))
            intcar3 = chr(intcar)
            intCar4 = hex(intcar)
            strOut += intcar3
        arr=bytes(strOut,'utf-8')
        return strOut


##########################################
# converte valuta da ascii in hex-ascii
##########################################
def convertCurrency(strIn):
        
        strOut=""
        x = strIn.split(";")
        unita = x[0]
        if (unita == "EUR"):
            strOut += "0006"
        elif (unita=="USD"):
            strOut += "0064"
        elif (unita=="UAH"):
            strOut += "0046"
        elif (unita=="CHF"):
            strOut += "0033"
        elif (unita=="GBP"):
            strOut += "0016"
        elif (unita=="IEP"):
            strOut += "0017"
        currency = x[2]
        strOut += convertLong2hex(currency).zfill(8)
        return strOut


##########################################
# converte campo peso da ascii in hex-ascii
##########################################

def convertWeight(strIn):
    strOut=""
    x = strIn.split(";")
    unita = x[0]
    decimali= x[1]
    if (decimali== "0"):
        strOut += "0000"
    elif (decimali == "-1"):
        strOut +="00FF"
    elif (decimali == "-2"):
        strOut +="00FE"
    elif (decimali == "-3"):
        strOut +="00FD"
    weight = x[2];
    strOut += convertLong2hex(weight).zfill(8)
    return strOut


#############################################
# converte sub funzione da ascii in hex-ascii
#############################################
def convertSubFunction(strIn):
        strOut=""
        subFunction= strIn[0:1]
        if subFunction=="G":
            strOut="0"
        if subFunction=="A":
            strOut="1"
        if subFunction=="P":
            strOut="3"
        if subFunction=="L":
            strOut="4"
        if subFunction=="D":
            strOut="5"
        if subFunction=="E":
            strOut="6"
        if subFunction=="S":
            strOut="7"
        if subFunction=="W":
            strOut="9"
        if subFunction=="X":
            strOut="A"
        if subFunction=="V":
            strOut="B"
        if subFunction=="M":
            strOut="D"

        subFunction= strIn[1:2]
        if subFunction=="X":
            strOut += "0"
        if subFunction=="W":
            strOut += "1"
        if subFunction=="L":
            strOut +="2"
        if subFunction=="D":
            strOut +="3"
        if subFunction=="V":
            strOut +="6"
        if subFunction=="T":
            strOut +="7"
        strOut += strIn[2:4]
        return strOut


#############################################
# converte un campo testo da ascii in hex-ascii
#############################################
def convertText2Hex(strIn):
        
        strOut=""
        valore=""
        c=0
        for i in strIn:
            valore= i
            if valore =="@":
                c+=1
                valore = strIn[c:c+2]
                strOut += valore
                c+=1
            else:
                strOut += dec2Any(ord(valore),16)
            c+=1
            
        if (len(strIn) % 2 != 0):
            strOut +="00"
        return strOut



#############################################
# converte un campo word da ascii in hex-ascii
#############################################
def convertWord2hex(strIn):
        strOut=""
        if (strIn == "-1") :
            strOut="FFFF"
        else:
            #strOut = dec2Any(strIn,16).zfill(8)
            a = int(strIn)
            strOut= f'{a:X}'.zfill(4)
            #hex_n = hex(a)
        return strOut


#############################################
# converte un campo Long da ascii in hex-ascii
#############################################

def convertLong2hex(strIn):
        strOut=""
        if (strIn == "-1") :
            strOut="FFFFFFFF"
        else:
            #strOut = dec2Any(strIn,16).zfill(8)
            
            a = int(strIn)
            strOut= f'{a:X}'.zfill(8)
            #hex_n = hex(a)
        return strOut

#############################################
# converte il numero di bytes della funzione
#############################################

def getNumByteText(strIn):
        
        strOut=""
        nbytes = len(strIn) - strIn.count("@") * 2
        hBytes = dec2Any(nbytes, 16)
        strOut = str(hBytes).zfill(4)
        return strOut

#############################################
# converte un numero da una base all'altra
#############################################

def any2Dec(number,base):
        
        index=0
        digits=""
        digitValue=0
        valore=""
        strOut=""
        ret = 0
        if (base<2 or base >36):
            strOut=""
        else:
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            digits = digits[:base]

        for i in range(len(number)):
            digitValue= str(i)
            valore =digits.find(digitValue)
            if valore>0:
                ret = ret*base + valore
        strOut=str(ret)       
        return strOut

#############################################
# converte un numero da una base all'altra
#############################################

def dec2Any(strNumber , base):
        
        index=0
        digits=""
        digitValue=0
        strOut=""
        
        number= int(strNumber)
        
        if (base<2 or base >36):
            strOut=""
        else:
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            digits = digits[:base]
        
        
        digitValue = int(number / base)
        valore = digits[digitValue :digitValue+1]
        strOut += valore
        
        number = number - int(digitValue*base)
        valore = digits[number :number+1]
        strOut += valore
        #print (strOut)
        
        return strOut

#################################################
# converte una subfunction da HEX-ASCII in ASCII
#################################################

def getFunzioneAscii(funzione):
    ret=""
    primaCifra = funzione[0:1]
    secondaCifra= funzione[1:2]
    
    d ={"0":"G","1":"A","3":"P","4":"L","5":"D","6":"E","7":"S","9":"W","A":"X","B":"V","D":"M"}
    ret=d[primaCifra]
    e = {"0":"X","1":"W","2":"L","3":"D","6":"V","7":"T"}
    ret += e[secondaCifra]
    
    ret += funzione[2:4]
    
    return ret

 
##########################################################################
# recupera la posizione di un token all'interno di una stringa
# in: strIn --> stringa ascii es. A!WV05|WW06|12|WW07|2|WL0A|5268|LX02
#     token --> WL0A
# out : strOut --> 3
##########################################################################
def takePositionFromString(strIn, token):
    a = strIn.split('|')
    for i in range(len(a)):
        if (a[i] == token):
            return i
    return 0

##########################################################################
# recupera il valore di un token all'interno di una stringa
# in: strIn --> stringa ascii es. A!WV05|WW06|12|WW07|2|WL0A|5268|LX02
#     token --> WL0A
# out : strOut --> 5268
##########################################################################
def takeValueFromString(strIn, token):
    a = strIn.split('|')
    for i in range(len(a)):
        if (a[i] == token):
            return a[i+1]
    return ""



###############################################################
# Converte una stringa ASCII in HEX-ASCII
# in: strIn --> stringa ascii es. A!GT02|PIPPO
# out : strOut --> D0510102.... 
###############################################################


def convertAscii2Hex(strIn , gxProfibus):
    strOut=''

    strIn = strIn.replace("A!","AWA|1|" + str(gxProfibus) +"|")
    strIn = strIn.replace("A?","ARA|1|" + str(gxProfibus) +"|")
    
    a=strIn.split("|")

    tipo=a[0]
    mittente = a[1]
    destinatario = a[2]
    primoComando = a[3]

    funzionePrimoComando= primoComando[1:2]
    if (tipo=="AWA"):
        strOut="D0"
    else:
        strOut="90"

    subFunction= "71"
    if funzionePrimoComando=="W":
        subFunction="77"
    if funzionePrimoComando=="L":
        subFunction="6C"
    if funzionePrimoComando=="D":
        subFunction="65"
    if funzionePrimoComando=="V":
        subFunction="51"
    if funzionePrimoComando=="T":
        subFunction="54"

    strOut += subFunction
    strOut += mittente.zfill(2)
    strOut += destinatario.zfill(2)
    try:

        funzione=""
        for i in range(3 , len(a)):
            funzione=a[i]
            subFunction=funzione[1:2]
            if (len(funzione) == 4):
                if (subFunction =="T"):
                    valore = a[i+1]
                    strOut += convertSubFunction(funzione)
                    strOut += getNumByteText(valore)
                    strOut += convertText2Hex(valore)     
                
                if (subFunction =="D"):
                    valore = a[i+1]
                    strOut += convertSubFunction(funzione)
                    x = valore.split(";")
                    if (x[0] =="KG"):
                        strOut += convertWeight(valore)
                    elif ( x[0] =="EUR"):
                        strOut += convertCurrency(valore)
                if (subFunction =="W"):
                    valore = a[i+1]
                    strOut += convertSubFunction(funzione)
                    if (funzione=="LW00"):
                        i +=1
                        valore = a[i]
                        strOut += convertSubFunction(funzione)
                        break
                    else:
                        strOut += convertWord2hex(valore).zfill(2)
                if (subFunction =="L"):
                    valore = a[i+1]
                    strOut += convertSubFunction(funzione)
                    strOut += convertLong2hex(valore).zfill(4)
                if (subFunction =="X"):
                    strOut += convertSubFunction(funzione)
                if (subFunction =="V"):
                    strOut += convertSubFunction(funzione)
                    if (i==3):
                        strOut +="XXXX"
                    else:
                        strOut +="0008"
            
        if (funzionePrimoComando == "V"):
            strToCount = strOut[strOut.find("XXXX")+ 4:]
            nbytes = len(strToCount)/2
            strOut = strOut.replace("XXXX", dec2Any(nbytes,16).zfill(4))
    except Exception as err:
        print (str(err))

    return strOut

#########################################################
# converte la stringa in ingresso strIn
# da HEX-ASCII in ASCII leggibile
# in : strIn
# out strOut
#########################################################

def convertHex2Ascii(strIn):
    strOut=""
    try:

        #if (strIn.find("BIZERBA_OK")) > -1:
        #    strIn = strIn.replace("BIZERBA_OK",'')
        #    if (strIn) =='':
        #        return "BIZERBA_OK"
            
        intestazione= strIn[0:8]
        if intestazione[0:2]=="D0":
            simbolo="!"
        else: 
            simbolo="?"
        strOut = "A" + simbolo
        
        idx=8
        while True:
            if (idx >= len(strIn)):
                break
            funzione = getFunzioneAscii(strIn[idx:idx +4])
            strOut += funzione + "|"
            mainFunction= funzione[0:1]
            subFunction = funzione[1:2]
            if (subFunction =="T"):
                idx +=4
                intNumBytes = int("0x" + strIn[idx:idx+4],0)
                idx +=4
                for i in range(idx,idx + intNumBytes*2,2):
                        valoreHex = int("0x" + strIn[i:i+2], 0)
                        strOut += chr(valoreHex)
                strOut +="|"
                idx +=intNumBytes * 2
                if (intNumBytes % 2 != 0):
                    idx +=2
            if (subFunction =="X"):
                idx +=4   
            if (subFunction =="W"):
                idx +=4
                if funzione =="LW00":
                    strOut +=  getFunzioneAscii(strIn[idx:idx +4]) 
                else:
                    hexValue =convertSubFunction(strIn[idx:idx +4])
                    strOut +=  str(int("0x" + hexValue, 0)) + "|"

                idx +=4
            if (subFunction =="V"):
                idx +=4
                intNumBytes = int("0x" + strIn[idx:idx+4],0)
                idx +=4     
            if (subFunction =="L"):
                idx +=4
                intNumBytes = int("0x" + strIn[idx:idx+8],0)
                strOut +=  str(intNumBytes) + "|" 
                idx +=8    
            if (subFunction == "D"):
                idx +=4
                intDimension = int("0x" + strIn[idx:idx+4],0)
                idx +=4
                dbl = int("0x" + strIn[idx:idx+8],0)
                if (intDimension > 200):
                    # peso 
                    if (intDimension == 253):
                        strOut += "KG;-3;"
                else:
                    # valuta
                    if (intDimension == 6):
                        strOut += "EUR;-2;"
                        
                strOut += str(dbl) + "|"
                idx +=8
    except Exception as e:
        print ("Errore " + str(e))
    return strOut


def parseGxNetString(strIn):
    funzione=""
    r = []
    d = strIn.split("|")
    for i in range(len(d)):
        funzione = d[i]    
        funzione= funzione.replace("A!","")
        if (isGxNetCommand(funzione)):
            if (funzione[1:2] == "V") or (funzione[1:2] == "X"):
                r.append(funzione)
            else:
                valore = d[i+1]
                r.append(funzione + "|" + valore)
                i+=1
    
    return r


        

def isGxNetCommand(strIn):
    sottofunzioni = "G,A,P,L,D,E,S,W,X,V,M"
    operandi = "X,W,L,D,V,T"
    if (len(strIn) !=4):
        return False
    else:
        if sottofunzioni.find(strIn[0:1])> -1 and operandi.find(strIn[1:1])> -1:
            return True
        else:
            return False
        
            
