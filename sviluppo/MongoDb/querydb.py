import pymongo
from pymongo import MongoClient

# eseguo la connessione
client = MongoClient('localhost',27017)
# apro un database di nome testdb
db = client.testdb
# chiedo di usare la collection persone
persone_coll = db.persone


#p = persone_coll.find_one()
#print(p)

persone = persone_coll.find({"nome": "Giuseppe"})
for persona in persone:
    print({persona["nome"]} , {persona["cognome"]})


res = persone_coll.update_one({"nome": "Giuseppe"},{"$set": {"eta": 50}})
p = persone_coll.find_one({"nome": "Giuseppe"})
print(p)

persona = persone_coll.find_one({"nome": {"$gt":"Giuseppe"}})
print(persona)

