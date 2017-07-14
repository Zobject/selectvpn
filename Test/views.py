#coding:utf8
import simplejson as simplejson
from django.shortcuts import render
from django.http import request ,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from itsdangerous import  URLSafeTimedSerializer
from rest_framework.parsers import JSONParser
import  pymongo
import  random
import string
import json
import httplib
# Create your views here.

try:
    conn=pymongo.MongoClient()
    print  'success'
except:
    print 'fail'
db=conn['VPN']

def encrypt(port,password):
    rule=URLSafeTimedSerializer('secret-key',salt='hello')
    token=rule.dumps({'port':port,'password':password,})
    return token

def encrypt1(port):
    rule=URLSafeTimedSerializer('secret-key',salt='hello')
    token=rule.dumps({'port':port})
    return token
def stopvpn(request):
    if request.method=='GET':
        if request.method == 'GET':
            #获取返回信息
            JiedianName = request.GET['name']
            port=request.GET['port']
            #给端口进行加密
            send_data = encrypt1(port)
            #判读具体的节点区域根据不同的节点信息给HOST进行赋值
            if JiedianName == 'US':
                collection = db.usa
                Host='13.59.235.45'

            elif JiedianName == 'EU':
                collection = db.eu

            elif JiedianName == 'AS':
                collection = db.jap
            # print port
            print collection.find_one({'port':int(port)})

            #向节点服务器发送关闭消息
            url = 'http://' + Host + ':1200/token=' + send_data
            print url
            #连接服务器
            conn = httplib.HTTPConnection(Host + ':1200')
            #发送get请求
            conn.request(method="GET", url=url)
            #获得返回数据
            response = conn.getresponse()
            res = response.read()
            #根据节点服务的返回进行不同的操作，如果返回成功对数据库进行更新将端口更新为可用，并且通知客户端。
            if res=='success':
                #更新数据库
                collection.update({'port': int(port)}, {'$inc': {'target': -1}})
                return JsonResponse({'reg':1,'target':'success'})
            else:
                #如果节点服务返回失败或者其他，不对节点列表进行操纵，返回给客户端失败让客户端进行。
                return  JsonResponse({'reg':0,'target':'fail'})
            print res
            print 'xxxxxxxxxxx'
        return JsonResponse({'target':1})

@csrf_exempt
def startvpn(request):
    if request.method=='POST':
        #判断连接具体某个节点服务器，和节点表
        Jiedianinfo=JSONParser().parse(request)
        JiedianName = Jiedianinfo.get('name')
        if JiedianName == 'US':
            collection=db.usa
            Host='13.59.235.45'
        elif JiedianName == 'EU':
            collection=db.eu
            Host = '52.56.168.139'
        elif JiedianName=='AS':
            collection=db.jap
            Host = '52.192.140.166'
        #从表中查询一条target为0（端口已存在但是未使用）的记录
        data=collection.find_one({'target':0})
        #如果没有数据
        if data==None:
            password=makepassword()
            #数据库中如果没有就利用1025端口
            if collection.find().count()==0:
                port=1025
            else:
            #数据库中如果存在就拿最后一个在用端口
                lastportdata=list(collection.find().skip(collection.find().count()-1).limit(1))
                for d in lastportdata:
                    port=d.get('port')+1
            #在最后一个在用端口+1开放给新的用户
            collection.insert({'ip':Host,'port':port,'target':1,'password':password})
            print port,Host,password
            #对端口进行加密
            send_data=encrypt(port,password)

        else:
            #如果有获取端口信息
            port=data.get('port')
            password=makepassword()
            Host=data.get('ip')
            #对端口信息加密
            send_data=encrypt(port,password)
            print port,password,Host
        print send_data
        url = 'http://'+Host+':1200/token='+send_data
        print url
        conn = httplib.HTTPConnection(Host+':1200')
        conn.request(method="GET", url=url)
        response = conn.getresponse()
        res = response.read()
        print res
        if res=='success':
            # 对端口信息进行更新
            collection.update({'port': port, 'ip': Host}, {'$set': {'target': 1, 'password': password}})
            return JsonResponse({'reg':1,'port': port, 'password': password})
        else:
            return JsonResponse({'reg':0,'target':'fail'})
        return JsonResponse({'target':1})


#生成6位密码
def makepassword():
    password=''.join(random.sample(string.ascii_letters+string.digits,5))
    return password
