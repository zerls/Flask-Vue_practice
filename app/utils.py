import redis,time,pickle
from datetime import datetime, timedelta

MAX_LIST=8
class Redis:
    @staticmethod
    def connect(host='localhost', port=6379, db=0):
        r = redis.StrictRedis(host, port, db)
        return r

    # 将内存数据二进制通过序列号转为文本流，再存入redis
    @staticmethod
    def set_data(r, key, data, ex=None):
        r.set(pickle.dumps(key), pickle.dumps(data), ex)

    # 将文本流从redis中读取并反序列化，返回
    @staticmethod
    def get_data(r, key):
        data = r.get(pickle.dumps(key))
        if data is None:
            return None

        return pickle.loads(data)
    
    @staticmethod
    def zadd(r, key,val):
        data = r.zadd(key,{pickle.dumps(val):time.time()})

    @staticmethod
    def zrange(re,key,l,r):
        datas=[]
        data= re.zrange(key,l,r)
        if data is None:
            return None
        for da in data:
            dd=pickle.loads(da)
            datas.append(dd)
        return  datas

    @staticmethod
    def lpush(re,key,data):
        if(data.get('time') != None):
            data['time']=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(data['time']))
        re.lpush(key,pickle.dumps(data))
        while re.llen(key) > MAX_LIST:
            _=re.rpop(key) 

    @staticmethod
    def lrange(re,key,l,r):
        datas=[]
        data=re.lrange(key,l,r)
        for da in data:
            dd=pickle.loads(da)
            datas.append(dd)
        return  datas
    