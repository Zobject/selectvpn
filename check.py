#coding:utf8
import pymongo
from  datetime import datetime
import time
import httplib
from  itsdangerous import URLSafeTimedSerializer



try:
    conn=pymongo.MongoClient()
    print 'success'
except:
    print 'fail'

db=conn['VPN']



def encrypt1(port):
    rule=URLSafeTimedSerializer('secret-key',salt='hello')
    token=rule.dumps({'port':port})
    return token


def check():
    while True:
        collection=db.usa
        data=list(collection.find({'target':1}))
        now=datetime.now()
        print "+++++++"
        for d in data:
            print d
            checktime=d.get('time')
            port=d.get('port')
            Host=d.get('ip')
            print port
            print Host
            #14400
            if (now-checktime).seconds>14400:
                print (now - checktime).seconds
                # print now
                print "+++++++"
                send_data = encrypt1(port)
                url = 'http://' + Host + ':1200/token=' + send_data
                print url
                # 连接服务器
                conn = httplib.HTTPConnection(Host + ':1200')
                # 发送get请求
                conn.request(method="GET", url=url)
                # 获得返回数据
                response = conn.getresponse()
                res = response.read()
                # 根据节点服务的返回进行不同的操作，如果返回成功对数据库进行更新将端口更新为可用，并且通知客户端。
                if res == 'success':
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
                send_data = encrypt1(port)
                url = 'http://' + Host + ':1200/token=' + send_data
                print url
                # 连接服务器
                conn = httplib.HTTPConnection(Host + ':1200')
                # 发送get请求
                conn.request(method="GET", url=url)
                # 获得返回数据
                response = conn.getresponse()
                res = response.read()
                # 根据节点服务的返回进行不同的操作，如果返回成功对数据库进行更新将端口更新为可用，并且通知客户端。
                if res == 'success':
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
                send_data = encrypt1(port)
                url = 'http://' + Host + ':1200/token=' + send_data
                print url
                # 连接服务器
                conn = httplib.HTTPConnection(Host + ':1200')
                # 发送get请求
                conn.request(method="GET", url=url)
                # 获得返回数据
                response = conn.getresponse()
                res = response.read()
                # 根据节点服务的返回进行不同的操作，如果返回成功对数据库进行更新将端口更新为可用，并且通知客户端。
                if res == 'success':
                    collection.update({'port': port, 'ip': Host},
                                  {'$set': {'target': 0, 'password': '3213213', 'time': datetime.now()}})
            else:
                print (now - checktime).seconds

                print now
        print 'xxxxxxxxxxx'
        time.sleep(1800)

if __name__ == '__main__':
    check()