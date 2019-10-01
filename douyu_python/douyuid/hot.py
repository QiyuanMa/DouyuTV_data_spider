import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'DYID'
# MONGO_TABLE = 'DouyuTV'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
uidpool = []

class MongodbConn(object):

    def __init__(self):
        self.CONN = pymongo.MongoClient('localhost')

    def run(self):
        database = "DYNOW1"
        db = self.CONN[database]
        col = db.collection_names()
        # the col is datbases list
        print(col)
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
                # print key of (key: value)
                global uidpool
                uidpool.append(i['uid'])
                print(i['uid'])
            # uidpool = list(set(uidpool))
                data={
                    '_id': i['uid'],
                    'rid': i['rid']
                }
                save_to_mongo(data, 'id_pool')

def save_to_mongo(result,table):
    try:
        if db[table].save(result):
            print('成功存储到mongodb', table)
    except Exception as e:
        print('存储到mongodb失败', e, table)

if __name__ == '__main__':
    mongo_obj = MongodbConn()
    mongo_obj.run()

