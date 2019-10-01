import socket
import re
import time
import requests
from pymongo import MongoClient
import datetime
import time
# 定时任务 # 设定一个标签 确保是运行完定时任务后 再修改时间



start = time.clock()
sk_client = socket.socket()

category = []
name = []
jdqscjzc =[]
jdqs = []

MONGO_URL = 'localhost'
MONGO_DB = 'DouyuTVnew'
# MONGO_TABLE = 'DouyuTV'
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    }
params = {
        'offset': 0,
        'limit': 100
    }

def main():
    try:
            response = requests.get('http://open.douyucdn.cn/api/RoomApi/live/jdqscjzc', params=params, headers=headers)
            if response.status_code == 200:
                html = response.text

                pattern = re.compile('"url":".*?com/(.*?)"', re.S)
                items = re.findall(pattern, html)
                for item in items:
                    data = {
                        "_id": item,
                        'owner_id': item,
                    }
                    save_to_mongo(data, 'jdqscjzc_id_pool')
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
                sched_timer = sched_timer + datetime.timedelta(minutes=10)
                print('next:',sched_timer)
                flag = 0
        end = time.time()
        # print('run time:', end - start, 's')

