try:
    import sys
    import time
    from datetime import datetime
    from time import sleep
    import socket
    import logging
    #from utility import * 
    from util import *
    from socket_connection import SocketConnection
    from gxnetFunction import *
    from configparser import ConfigParser
    
    #from elabora_dati import Elabora
except ImportError as e:
    print('[!] Failed to import bizerba: %s' % e)
    exit(1)

class Bizerba:
    def __init__(self, device, config=''):

        self.socketConnection = SocketConnection()
        self.device = device
        self.config = config


    def read_etcd(self):
        self.batchId = '01:01:13:3:1684656656' #MATTEO DEBUG
        self.sku = '16750' #MATTEO DEBUG
        #Da fare tramite API non più etcd
        print("leggo il batch in corso......")
        

    def get_vendor(self):
        return self.vendor

    def get_model(self):
        return self.model

    def is_connected(self):
        return self.socketConnection.connected

    def check_correct_configuration(self, expected_config):
        self.ping_device()
        self.read_etcd()
        # Controlla che il seriale / mac address / ip sia quello presente nella expected_config
        return True  # Ritorna True se la configurazione e' corretta, altrimenti False

    def reconnect(self):
        host = self.device['ip']
        port = int(self.device['port'])
        self.socketConnection.setConfig(self.config, host, port)
        self.socketConnection.connect()
        logga(self, "Connected to device")

    def reload_device(self):
        self.socketConnection.stop()
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        self.reconnect()

      # Invio dati al device
    def send_data(self, data, term=""):
        print("SENDDATA: "+ data )
        if(data!='BIZERBA_OK'):
            print(convertHex2Ascii(data) )
        sent = self.socketConnection.send(data.encode(),"")
        print("Data sent") if sent else print("Didn't send data")

    # Lettura dati dal device
    def read_data(self):
        try:
            data = self.socketConnection.read()
            if(data is False):
                print(self, "Connection reset")
                return self.read_data()
            if (data!=''):
                # Bizerba Deve rispondere "BIZERBA_OK"
                self.send_data("BIZERBA_OK")
                data = data.decode("UTF-8")
                #print("READ: "+data_)
                
                # La bilancia ha risposto OK quindi ha recepito il comando
                if(data.find("BIZERBA_OK")) > -1:
                    data = data.split("BIZERBA_OK")[1]
                    
                logga(self, "RECEIVED FROM DEVICE %s " % data )
                logga(self, convertHex2Ascii(data))
                return data
            else:
                 return ''    
        except BlockingIOError:
            logga(self, "blocking socket exception")

    def get_statistical_data(self): # chiede i dati statistici assoluti 
        #self.send_data('')
        #self.send_data("A!LV01|GT02|CIAO " + str(datetime.now()) + "|GD10|EUR;-2;" + str(100) + "|GD01|KG;-3;" + str(100) + "|LX02")
        self.send_data(self.__adattaStringaPerHexAscii("A?WV30|1"))
        #self.change_Plu()

        pass
        
    def get_sku_local(self): # Lista sku locali
        self.send_data('')
    
    def change_Plu(self): # cambia il plu
         pluNumber ="2"
         self.send_data(self.__adattaStringaPerHexAscii("A!XV00|GL19|" + pluNumber + "|LX02"))


    def ping_device(self):
        if(self.init):
            self.send_data(self.__adattaStringaPerHexAscii("A?PL03|0"))
            #pass
        
    def set_init(self):
        msg= 'BIZERBA_TCP_INFO'
        msg += chr(4)
        msg += chr(21)
        msg += chr(1)
        msg += chr(0)
        msg += chr(1) #self.clientSyncn se vale 1 ricevo o invio BIZERBA_OK
        msg += chr(1) #self.clientConversion 2 = in chiaro 1 = binario
        msg += chr(124)
        msg += chr(64)
        self.init = True
        self.send_data(msg)
    

    def set_time(self):
        #self.send_data('')
        button3test ="A!WV04|WW06|3|WW07|0|WW08|1|WT00|TEST|LX02"
        self.send_data(self.__adattaStringaPerHexAscii(button3test))

        pass

    def check_sku_change(self,new_sku):
        return check_sku_change(self.sku, new_sku)

    def send_to_stream_event(self, event_key, data): # Manda i dati sugli stream rabbitmmq
        # Stream event per device/gateway
        if(data is not None):
            #print(event_key)
            #self.eventproducer.send_message(event_key, json.dumps(data))
            return True
        
    def __adattaStringaPerHexAscii(self, str2Send):
        #str2Send = str2Send.replace("A!","AWA|1|2|")
        #str2Send = str2Send.replace("A?","ARA|1|2|") 
        strOut = convertAscii2Hex(str2Send)
        return strOut
    
    def build_stats_batch(self,dati,structure):
        stats_dict = defaultdict(dict)    
        structure["timestamp"] = dati["timestamp"]
        structure["id"] = dati["batchId"]
        structure["counters"]["unchecked"]["metal"] = dati["metal"]
        structure["counters"]["unchecked"]["special"] = dati["special"]
        structure["counters"]["unchecked"]["xray"] = dati["xray"]  if dati["xray"] !='' else 0
        structure["counters"]["checked"]["packages"]["T++"] = dati["T++"] if '-' not in dati["T++"] else 0
        structure["counters"]["checked"]["packages"]["T+"] = dati["T+"] if '-' not in dati["T+"] else 0
        structure["counters"]["checked"]["packages"]["T"] = dati["T"] if '-' not in dati["T"] else 0
        structure["counters"]["checked"]["packages"]["T-"] = dati["T-"] if '-' not in dati["T-"] else 0
        structure["counters"]["checked"]["packages"]["T--"] = dati["T--"] if '-' not in dati["T--"] else 0
        structure["counters"]["checked"]["accepted"]["total"] = dati["accepted"]
        structure["counters"]["checked"]["accepted"]["legalUnderweight"] = dati["accepted_T-"]
        structure["counters"]["checked"]["rejected"]["under"] = int(dati["rejected"])-int(dati["T+"])
        structure["counters"]["checked"]["rejected"]["over"] = int(dati["rejected"]) - int(structure["counters"]["checked"]["rejected"]["under"])
        structure["counters"]["checked"]["rejected"]["special"] = dati["special"]
        structure["counters"]["checked"]["rejected"]["metal"] = dati["metal"]
        structure["counters"]["checked"]["rejected"]["xray"] = dati["xray"]  if dati["xray"] !='' else 0
        structure["weights"]["checked"]["packages"]["T++"] = round(float(dati["T++_Weight"])*1000*1000) if '-' not in dati["T++_Weight"] else 0
        structure["weights"]["checked"]["packages"]["T+"] = round(float(dati["T+_Weight"])*1000*1000) if '-' not in dati["T+_Weight"] else 0
        structure["weights"]["checked"]["packages"]["T"] = round(float(dati["T_Weight"])*1000*1000) if '-' not in dati["T_Weight"] else 0
        structure["weights"]["checked"]["packages"]["T-"] = round(float(dati["T-_Weight"])*1000*1000) if '-' not in dati["T-_Weight"] else 0
        structure["weights"]["checked"]["packages"]["T--"] = round(float(dati["T--_Weight"])*1000*1000) if '-' not in dati["T--_Weight"] else 0
        structure["weights"]["checked"]["accepted"]["total"] = round(int(dati["accepted"])*float(dati["averageWeight"])*1000)
        structure["weights"]["checked"]["accepted"]["averageWeight"] = round(float(dati["averageWeight"])*1000)
        structure["weights"]["checked"]["accepted"]["stdDev"] = round(float(dati["stdDev"])*1000)
        
        stats_dict["stats"] = structure
        return stats_dict

class B(Bizerba):
    def get_model():
        print (self.model)
        
        

        
    def retrieve_missed_data(self):
        # TODO: check if any data has not been read yet
        # TODO: this has to return the missed_data if there is any, otherwise return False
        missed_data = []
        return False

    # Da usare solo per comandi spontanei ricevuti dal device!!!!! verifica se il dato ricevuto è da considerarsi un comando
    def is_command(self, data):
        line = convertHex2Ascii(data)
        """
        for dati in line:
            check_command = dati.split(' ')
            if (len(check_command[0]) > 0 and check_command[0] in template.key_command): # cerco nei template se la chiave è da considerarsi un comando
                return True # -> è un comando ricevuto dalla bilancia tipicamente cambio articolo
            else:
                return False
        """
        return False
    
    # Da usare solo per comandi spontanei ricevuti dal device!!!!! 
    def manage_command(self, data): # Invia i comandi creati con build_send alla bilancia
        command = data.split(' ')
       
        self.comando = self.build_send(command[0].strip("\r\n"), command[1].strip("\r\n")) # Restituisce il comando/i da inviare

        for comando in self.comando:
            if(comando !='timestamp' and comando !='production_end'):
                self.send_data(self.comando[comando])   
                #self.read_data()
        print(self.comando)
        
        return True

    
    def build_send(self, key_received, key_values): # prepara le risposte da inviare alla bilancia in base alle richieste ricevute

        val = getValues(self.id_device, self.sku) # Mi restituisce i dati articolo
        values = val.copy()
        
        # Importante!!!! Sulla bilancia invio il batchId
        if(self.batchId!=''):
            values['batch_name'] = self.batchId.split(":")[4]
        sequenza = template.command_sequence[key_received]
        key_structure = template.key_structure
        key_values = template.key_values
        esito = defaultdict(dict)
        
        del (sequenza)
        del (values)
        print_string = ''
        esito.update({"timestamp": getGMTmicro()})
        return esito

    def processes_receive(self,data): # Processa i dati ricevuti dalla bilancia tramite read_data
        dati_elaborati = defaultdict(dict)
        dati = defaultdict(dict)
        
        dati = convertHex2Ascii(data)
        
        print(dati) 
        
        statistical_data = template.statistical_data
        
        chiavi_split = template.chiavi_split
        
        finito = False
        #for riga in line:
        
        # Ritorna dict chiave valore
        return dati_elaborati
    

config = ConfigParser()
config.read('config.ini')
device ={'ip': '192.168.68.200', 'port' : '1045'}
b = Bizerba(device, config)

b.reconnect()


b.send_data("A?PL03|0")
data=""
while data == "":
    data =b.read_data()
    time.sleep(0.2)
    
print (data)


