from flask_apscheduler import APScheduler
from .utils import Redis
from .models import Data,Data_type,Place,Collector
import time
from . import rredis,db

def task1():

    a,b=time.time(), time.asctime( time.localtime(time.time()) )

    place="河口"
    types="温度"
    strkey=str(place)+"::"+str(types) 
    data_l=Redis.zrange(rredis,strkey,0,10) 
    if(rredis.zcard(strkey) >= 2):
        for data in data_l:
            content=data['data'],
            place = Place.query.filter_by(name=place).first()
            types_ = Data_type.query.filter_by(name=types).first()
            col = Collector.query.filter_by(id=data['data_collector']).first()

            d = Data(content=content, data_type=types_,data_place=place, data_collector=col,time=data['time'])
            db.session.add(d)
        db.session.commit()
        print("task1::OK",strkey)

