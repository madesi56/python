import importlib
import binascii
import logging
import time
import smtplib
import re
from email.mime.multipart import MIMEMultipart
import json
import os.path
from collections import namedtuple
from datetime import datetime,timedelta
import uuid

def load_module(modulename):
    mod = None
    #print("MODULE NAME "+modulename)
    try:
        mod = importlib.import_module(modulename)
    except ImportError:
        print("Failed to load {module}")
    return mod


def hexdec(value):
    return int(value, base=16)


def hex2bin(value):
    return binascii.unhexlify(value)


def int2bin(value, b_type='big', signed='False', nbyte=2):
    return value.to_bytes(nbyte, b_type, signed=signed)


def byte2int(value, b_type='big', signed='False'):
    return int.from_bytes(value, b_type, signed)

def get_uuid():
    # make a UUID based on the host ID (Mac Address) and current time
    return uuid.uuid1()

def clear_charset(s):
    s.strip()
    s = re.sub(r'[^A-Za-z0-9 ]', '', s)
    return s


def invia_mail(testo):
    msg = MIMEMultipart()
    msg['From'] = ''
    msg['To'] = ''
    msg['Subject'] = testo
    server = smtplib.SMTP('', '25')
    server.ehlo()
    text = msg.as_string()
    # server.sendmail("srvmoretta@rana.it", "g935zhxnuu@pomail.net", text)
    server.quit()


def logga(self, stringa=''):
    print('[%s]\t %s' % (time.strftime("%d/%m/%Y %H:%M:%S"), stringa))
    #self.log.info('[%s]\t %s' % (time.strftime("%d/%m/%Y %H:%M:%S"), stringa))


def json_load_fromfile(filename):
    if (os.path.isfile(filename)):
        f = open(filename)
        data = json.load(f)
        data_str = json.dumps(data)
        # Creo un json object analogo al dato generato dal database
        x = json.loads(data_str, object_hook=lambda d: namedtuple('X', d.keys())
                       (*d.values()))
        f.close()
        # print(x)
        return x
    else:
        return []


def add_dict_key(data, key, value):
    data[key] = value
    return data


def get_date(d_format="%d.%m.%Y"):
    today = datetime.today()
    dt_string = today.strftime(d_format)
    return dt_string


def get_hour(d_format="%H.%M.%S"):
    now = datetime.now()
    dt_string = now.strftime(d_format)
    return dt_string

def fillbytes(value=0):
    return bytes(value)

def strtoBinary(value):
  l,m=[],[]
  for i in value:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

def getGMTmicro():
    return time.time()

def getGMT():
    return int(time.time())

def create_batch_ID(sku, id_device, line):
    return {'sku':sku, 'line':line, batch_id: getGMT(),'id_device':id_device}

def get_line_sku(sku, sku_length=5, separator='', line=''):
    code = sku
    if(separator==''):
        step_split = sku_length
        if (len(sku.strip())>sku_length):
            line = sku[:-step_split].strip()
            code = sku[-step_split:].strip()
        else:
            code = sku.strip()
            #line = line
    else:
        elements = sku.split(separator)
        line = elements[0]
        code = elements[1]
    return {'line':line,'sku':code}

def check_sku_change(actual,new):
    if(actual != new):
        return True
    return False


def calculate_expire_date(self,val):
        if(val["tipo_scadenza"]=='W'):#monday this week
            now = datetime.now()
            monday = now - timedelta(days = now.weekday())
            newdate = monday + timedelta(days=int(val["shlife"]))
            return newdate #newdate.strftime(val["date_format"])
        
        if(val["tipo_scadenza"]=='D' or val["tipo_scadenza"]=='A'):
            now = datetime.now()
            newdate = now + timedelta(days=int(val["shlife"]))
            return newdate #newdate.strftime(val["date_format"])

def build_requestID():
    return str(get_uuid())

def build_item_load_request(id_device,line,sku):
    return {
    'event': {
        'timestamp': getGMT(), 
        'requestId': build_requestID(),
        'event':"itemLoadRequest", 
        'source':'device',
        'plant': '',
        'device': id_device,
        'line':line,
        'SKU':sku,
        'unit': '',
        'targetQuantity': ''
        }
    }

def build_item_loaded(id_device,line,sku,requestId):
    return {
        'event': {
            'timestamp': getGMT(),
            'event': 'itemLoaded',
            'requestId': requestId, 
            'plant': '',
            'device': id_device,
            'line': line,
            'SKU': sku,
            'response': 'OK'
        }
    }


def build_item_notloaded(id_device,line,sku,requestId,error):
    return {
        'event': {
            'timestamp': getGMT(),
            'event': 'itemNotLoaded',
            'requestId': requestId, 
            'plant': '',
            'device': id_device,
            'line': line,
            'SKU': sku,
            'response': 'KO',
            'errorCode': error
        }
    }

def build_batch_start(id_device,line,sku,requestId,batchId):
    return {
        'event': {
            'timestamp': getGMT(),
            'event': 'batchStart',
            'requestId': requestId, 
            'plant': '',
            'device': id_device,
            'line': line,
            'SKU': sku,
            'id': batchId # batchId -> tenantId:stabilimento:linea:deviceMaster:timestamp
        }
    }

def create_batch_Id(line,id_device,batch_timestamp):
    # me lo da Etcd tenantID e stabilimento?
    tenantId = '1'
    stabilimento = '1'
    #+":"+str(line)
    return  str(tenantId)+":"+str(stabilimento)+":"+str(id_device)+":"+str(batch_timestamp)


def build_error_received(id_device, line, sku, batchId='', error=''):
    return {
        'event': {
            'timestamp': getGMT(),
            'event': 'errorReceived',
            'id': batchId,
            'plant': '',
            'device': id_device,
            'line': line,
            'SKU': sku,
            'source':'device',
            'errorCode': error
        }
    }

# rabbitmq 100.126.1.2:15672 admin/netlite
#gateway redis simulato  


def build_batch_stop_request(id_device,line,sku):
    return {
        'event': {
        'timestamp':  getGMT(),
        'requestId': build_requestID(),
        'event': 'batchStopRequest',
        'plant': '',
        'source': 'device',
        'device': id_device,
        'line': line
        }
    }
    

def build_batch_stop(id_device,line,sku,requestId):
    return {
        'event': {
        'timestamp': getGMT(),
        'requestId': requestId,
        'event': 'batchStopped',
        'plant': '',
        'device': id_device,
        'line': line,
        'response': 'OK'
        }
    }

    
    
batch_stats_structure = {
    'timestamp': '', # timestamp GMT
    'id': '',
        "counters" :{
            "unchecked": {
                "special": "",
                "metal": "",
                "xray": ""
            },
            "checked": {
                "packages": {
                    "T++": "",
                    "T+": "",
                    "T": "",
                    "T-": "",
                    "T--": ""
                },
                "accepted": {
                    "total": "",
                    "legalUnderweight": ""
                },
                "rejected": { 
                    "over": "",
                    "under": "",
                    "special": "",
                    "metal": "",
                    "xray": ""
                }
            }

        },
        "weights" :{
            "checked": {
                "packages": {
                    "T++": "",
                    "T+": "",
                    "T": "",
                    "T-": "",
                    "T--": ""
                },
                "accepted": {
                    "total": "",
                    "legalUnderweight": ""
                }
            }
        }
}

# rabbitMq queue

events_type = {"events","stats","command"}

events_key ={"events":".events","stats":".*.stats","command":".command"}

queue_declare_args = {
            "events": {"x-queue-type": "stream",
                "x-max-length-bytes": 1_000_000,
                "x-stream-max-segment-size-bytes": 100_000,
                "x-max-age": "1Y"},
            "stats": {
                "x-queue-type": "stream",
                "x-max-length-bytes": 2_000_000,
                "x-stream-max-segment-size-bytes": 100_000,
                "x-max-age": "6M"},
            "command": {
                "x-queue-type": "quorum",
                "x-message-ttl": 300,
                "x-max-length": 10}
}

