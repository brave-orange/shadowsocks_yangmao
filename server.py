#!/usr/bin/env python
# encoding=utf-8
# 
# 跑在服务器上的脚本,用于博客上获取节点信息,以及在线配置下发
from flask import Flask, jsonify, request, make_response
from flask_cors import *
from myRedis import *
from config import *
import hashlib,json
# Instantiate our Node
app = Flask(__name__)
CORS(app, supports_credentials=True)
redis = RedisDb(config['redis']['host'],config['redis']['port'],config['redis']['password'])
LOCKKEY = "clent-ip-%s"
HOSTSKEY = "check_ware"
@app.route('/getSsr', methods=['GET'])
def getSsr():       #获取节点
    clentIp = request.remote_addr
    if redis.get(getLockKey(clentIp)):
        response = {'code': 1,"msg":f"请求频繁,请稍等"}
        return jsonify(response), 200
    getIpLock(clentIp)
    host = redis.lpop(HOSTSKEY)
    if not host:
        response = {'code': 1,"msg":f"当前没有资源"}
        return jsonify(response), 200
    else:
        redis.rpush(HOSTSKEY,host)    #用过的给他放到后面去,保证资源被均匀用到
    response = {'code': 0,"msg":f"success","data":json.loads(host)}
    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers']='*'
    return res, 200

@app.route('/Delivery', methods=['GET','POST'])
def configDelivery():
    sConfig = {
        "version": "4.3.1.0",
        "configs":[]
    }
    data = request_parse(request)
    if data.get("app_token") == config["app_token"]:
        servers = []
        res = redis.lrange(HOSTSKEY,0,-1)
        for item in res:
            item = json.loads(item)
            servers.append({
                  "server": item["host"],
                  "server_port": item["port"],
                  "password": item["password"],
                  "method": item["method"],
                  "plugin": "",  
                  "plugin_opts": "",
                  "remarks": "",
                  "timeout": 5
                 }) 
        sConfig['configs'] = servers
    res = make_response(jsonify(sConfig))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers']='*'
    return res, 200
def request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data
def getIpLock(ip):
    key = getLockKey(ip)
    res = redis.set(key,1,3)
def getLockKey(ip):
    m = hashlib.md5()
    rKey = LOCKKEY%(ip)
    rkey = rKey.encode(encoding='utf-8')
    m.update(rkey)
    keyMd5 = m.hexdigest()
    return keyMd5
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25025)
