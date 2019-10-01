import socket
import re
import time
import requests
from pymongo import MongoClient

start = time.clock()
sk_client = socket.socket()

category = []
name = []
jdqscjzc =[]
jdqs = []

MONGO_URL = 'localhost'
MONGO_DB = 'DouyuTVTest3'
MONGO_TABLE = 'DouyuTV'
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    }
params = {
        'offset': 0,
        'limit': 10000
    }

def main():
    get_name()
    i =0
    try:
        for element in category:
            response = requests.get('http://open.douyucdn.cn/api/RoomApi/live/'+element, params=params, headers=headers)
            if response.status_code == 200:
                html = response.text
                pattern = re.compile('"room_id":(.*?),.*?"room_name":"(.*?)","owner_uid":"(.*?)".*?"hn":(.*?),'
                                     + '"nickname":"(.*?)","url":".*?com/(.*?)"', re.S)
                items = re.findall(pattern, html)
                for item in items:
                    data = {
                        'room_id': item[0],
                        'room_name': item[1],
                        'owner_uid': item[2],
                        'hn': item[3],
                        'nickname': item[4],
                        'url': item[5],
                    }
                    save_to_mongo(data, name[i])
                    if element == 'jdqscjzc':
                        jdqscjzc.append(item[5])
            i = i+1
    except Exception as e:
        print(e)
    get_detail()

def get_name():
    try:
        response = requests.get('http://open.douyucdn.cn/api/RoomApi/game', params=params, headers=headers)
        if response.status_code == 200:
            html = response.text
            pattern = re.compile('"game_name":"(.*?)","short_name":"(.*?)",', re.S)
            items = re.findall(pattern, html)
            for item in items:
                name.append(item[0])
                category.append(item[1])
        print(category)
    except Exception as e:
        print(e)

def get_detail():
    try:
        for i in range(1,30):
            response = requests.get('http://open.douyucdn.cn/api/RoomApi/room/'+jdqscjzc[i], params=params, headers=headers)
            if response.status_code == 200:
                html = response.text
                print(html)
                pattern1 = re.compile('"room_id":"(.*?)".*?"cate_name":"(.*?)","room_name":"(.*?)",'
                                      +'"room_status":"(.*?)","start_time":"(.*?)","owner_name":"(.*?)",'
                                       +'.*?"hn":(.*?),"owner_weight":"(.*?)","fans_num":"(.*?)",', re.S)

                items1 = re.findall(pattern1, html)
                if items1:
                    print('1')
                pattern2 = re.compile('gift.*?"id":"(.*?)".*?name":"(.*?)".*?type":"(.*?)".*?pc":(.*?),.*?gx":(.*?),',re.S)
                items2 = re.findall(pattern2, html)
                if items2:
                    print('2')
                for item1 in items1:
                    print('3')
                    for item2 in items2:
                        print('4')
                        data = {
                            'room_id': item1[0],
                            'cate_name': item1[1],
                            'room_name': item1[2],
                            'room_status': item1[3],
                            'start_time': item1[4],
                            'owner_name': item1[5],
                            'gift_id': item2[0],
                            'gift_name': item2[1],
                            'gift_type': item2[2],
                            'gift_pc': item2[3],
                            'gift_gx': item2[4],
                        }
                        save_to_mongo(data, jdqscjzc[i])
    except Exception as e:
        print(e)

def save_to_mongo(result,table):
    try:
        if db[table].insert(result):
            print('成功存储到mongodb', table, result)
    except Exception:
        print('存储到mongodb失败', table, result)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('run time:', end - start, 's')

