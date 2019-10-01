import socket
import re
import time
import requests
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'DYID'
# MONGO_TABLE = 'DouyuTV'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
ridpool = []

start = time.clock()
sk_client = socket.socket()

category = []
name = []
jdqscjzc =[]
jdqs = []

MONGO_URL = 'localhost'
MONGO_DB = 'Detail_Info'
MONGO_TABLE = 'detail_info'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    }
params = {
        'offset': 0,
        'limit': 100
    }

class MongodbConn(object):

    def __init__(self):
        self.CONN = pymongo.MongoClient('localhost')

    def run(self):
        database = "DYID"
        db = self.CONN[database]
        col = db.collection_names()
        # the col is datbases list
        print(col)
        global num
        num = db['id_pool'].find().count()
        print(num)
        for element in col:
            #this is a database, in list loc 4
            col = element
            collection = db.get_collection(col)
            # query one document
            # document = collection.find_one()
            # print(document)
            # query all document
            documents = collection.find()
            for i in documents:
                global ridpool
                ridpool.append(i['rid'])
                # print(i['rid'])

def get_detail():
    try:
        for i in range(1, num):
            response = requests.get('http://open.douyucdn.cn/api/RoomApi/room/'+ridpool[i], params=params, headers=headers)
            if  response.status_code == 200:
                html = response.text
                pattern1 = re.compile('"room_id":"(.*?)".*?"cate_name":"(.*?)","room_name":"(.*?)",'
                                      +'"room_status":"(.*?)","start_time":"(.*?)","owner_name":"(.*?)",'
                                       +'.*?"hn":(.*?),"owner_weight":"(.*?)","fans_num":"(.*?)",', re.S)

                items1 = re.findall(pattern1, html)
                for item1 in items1:
                    if item1[3]=='1':
                        data = {
                            'room_id': item1[0],
                            'cate_name': item1[1],
                            'room_name': item1[2],
                            'room_status': item1[3],
                            'start_time': item1[4],
                            'owner_name': item1[5],
                            'hn':item1[6],
                            'owner_weight': item1[7],
                            "fans_num": item1[8],
                        }
                        save_to_mongo(data, item1[0])
    except Exception as e:
        print(e)

def save_to_mongo(result,table):
    try:
        if db[table].insert(result):
            print('成功存储到mongodb', table, result)
    except Exception:
        print('存储到mongodb失败', table, result)

if __name__ == '__main__':
    # start = time.time()
    # main()
    # end = time.time()
    # print('run time:', end - start, 's')
    mongo_obj = MongodbConn()
    mongo_obj.run()
    get_detail()

