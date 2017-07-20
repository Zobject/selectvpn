import pymongo
from datetime import  datetime ,timedelta

try:
    conn=pymongo.MongoClient()
    print  'success'
except:
    print 'fail'
db=conn['VPN']

collection=db.usa
d1=datetime.now()
collection.insert({'ip':'13.59.85.139','port':1059,'target':1,'password':'lSlZ1h','time':d1+timedelta(days=34501)})
collection=db.eu
collection.insert({'ip':'52.192.140.166','port':1059,'target':1,'password':'lSlZ1h','time':d1+timedelta(days=34501)})
collection=db.jap
collection.insert({'ip':'52.56.168.139','port':1040,'target':1,'password':'lSlZ1h','time':d1+timedelta(days=34501)})