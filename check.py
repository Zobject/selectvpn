import pymongo
from  datetime import datetime ,timedelta
import time

try:
    conn=pymongo.MongoClient()
    print 'success'
except:
    print 'fail'

db=conn['VPN']


def check():
    while True:
        collection=db.usa
        data=list(collection.find({'target':1}))
        now=datetime.now()
        for d in data:
            print d
            checktime=d.get('time')
            port=d.get('port')
            Host=d.get('ip')
            print port
            print Host
            #14400
            if (now-checktime).seconds>14400:
                # print (now-checktime).seconds
                # print now
                print "+++++++"
                collection.update({'port': port, 'ip': Host},
                                  {'$set': {'target': 0, 'password': '3213213', 'time': datetime.now()}})
        # time.sleep(1800)

        collection=db.eu
        data = list(collection.find({'target': 1}))
        now = datetime.now()
        for d in data:
            print d
            checktime = d.get('time')
            port = d.get('port')
            Host = d.get('ip')
            print port
            print Host
            # 14400
            if (now - checktime).seconds > 14400:
                print (now - checktime).seconds
                # print now
                print "+++++++"
                collection.update({'port': port, 'ip': Host},
                                  {'$set': {'target': 0, 'password': '3213213', 'time': datetime.now()}})
            else:
                print (now - checktime).seconds
                print now
        # time.sleep(1800)

        collection=db.jap
        data = list(collection.find({'target': 1}))
        now = datetime.now()
        for d in data:
            print d
            checktime = d.get('time')
            port = d.get('port')
            Host = d.get('ip')
            print port
            print Host
            # 14400
            if (now - checktime).seconds > 14400:
                print (now - checktime).seconds
                # print now
                print "+++++++"
                collection.update({'port': port, 'ip': Host},
                                  {'$set': {'target': 0, 'password': '3213213', 'time': datetime.now()}})
            else:
                print (now - checktime).seconds
                print now
        time.sleep(1800)

if __name__ == '__main__':
    check()