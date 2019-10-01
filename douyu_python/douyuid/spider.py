import urllib.request
import re
import socket
from pymongo import MongoClient
import datetime
import time

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

start = time.clock()
sk_client = socket.socket()
category = []
name = []
jdqscjzc =[]
jdqs = []
MONGO_URL = 'localhost'
MONGO_DB = 'DYNOW1'
# MONGO_TABLE = 'DouyuTV'
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'content-encoding': 'gzip',
    'content-type': 'application/json; charset=utf-8',
}
def main():
    try:
        tag = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(1,250):
            request = urllib.request.Request("https://www.douyu.com/gapi/rkc/directory/0_0/"+str(i), headers=headers)
            response = urllib.request.urlopen(request)
            if response.code == 200:
                doc = response.read().decode('utf-8')
                pattern = re.compile('"rid":(.*?),.*?"uid":(.*?),"nn":"(.*?)",.*?"ol":(.*?),.*?"c2name":"(.*?)"', re.S)
                items = re.findall(pattern, doc)
                for item in items:
                    data = {
                        "_id": item[1],
                        'rid': item[0],
                        'uid': item[1],
                        'nn': item[2],
                        'fan': item[3],
                        'tag': item[4],
                    }
                    save_to_mongo(data, tag)

        # for i in range(1,15):
        #     request = urllib.request.Request("https://www.douyu.com/gapi/rkc/directory/2_1/"+str(i), headers=headers)
        #     response = urllib.request.urlopen(request)
        #     if response.code == 200:
        #         doc = response.read().decode('utf-8')
        #         pattern = re.compile('"rid":(.*?),', re.S)
        #         items = re.findall(pattern, doc)
        #         for item in items:
        #             data = {
        #                 "_id": item,
        #                 'owner_id': item,
        #             }
        #             save_to_mongo(data, '英雄联盟')
        #
        # for i in range(1, 6):
        #     request = urllib.request.Request("https://www.douyu.com/gapi/rkc/directory/2_201/" + str(i), headers=headers)
        #     response = urllib.request.urlopen(request)
        #     if response.code == 200:
        #         doc = response.read().decode('utf-8')
        #         pattern = re.compile('"rid":(.*?),', re.S)
        #         items = re.findall(pattern, doc)
        #         for item in items:
        #             data = {
        #                 "_id": item,
        #                 'owner_id': item,
        #             }
        #             save_to_mongo(data, '颜值')

    except Exception as e:
        print(e)

def save_to_mongo(result,table):
    try:
        if db[table].save(result):
            print('成功存储到mongodb', table, result)
    except Exception:
        print('存储到mongodb失败', table, result)

if __name__ == '__main__':
    flag = 0
    # 获取当前时间
    now = datetime.datetime.now()  # 启动时间 # 启动时间为当前时间 加5秒
    sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                    now.second) + datetime.timedelta(seconds=5)
    while (True):  # 当前时间
        start = time.time()
        now = datetime.datetime.now()
        if sched_timer < now < sched_timer + datetime.timedelta(seconds=5):
            time.sleep(1)
            main()
            flag = 1
        else:
            if flag == 1:
                sched_timer = sched_timer + datetime.timedelta(minutes=15)
                print('next:', sched_timer)
                flag = 0
        end = time.time()
        # print('run time:', end - start, 's')