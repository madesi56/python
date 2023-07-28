import pymongo
from pymongo import MongoClient

# eseguo la connessione con MongoDb
client = MongoClient('localhost',27017)
#creo un database e lo chiamo testdb
db = client.testdb
# creo la collection persone
persone_coll = db.persone
# creo indici
persone_coll.create_index([("nome",pymongo.ASCENDING)])
persone_coll.create_index([("cognome",pymongo.ASCENDING)])
persone_coll.create_index([("computer",pymongo.ASCENDING)])

# creo il primo documento
p1 = {"nome" : "Mario" , "cognome" : "Rossi" , "eta" : 30 , "computer" : ["apple","asus"]}
# inserire il doc in mongodb
persone_coll.insert_one(p1)
p2 = {"nome" : "Giuseppe" , "cognome" : "Verdi" , "eta" : 45 , "computer" : ["asus"]}
persone_coll.insert_one(p2)
p3 = {"nome" : "Franco" , "cognome" : "Giugliani" , "eta" : 65 , "computer" : ["asus","apple"]}
persone_coll.insert_one(p3)

