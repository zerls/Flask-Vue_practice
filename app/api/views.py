from flask import jsonify, request, current_app, url_for
from . import api
from .. import db, rredis
from ..models import Collector, Collect_state, Collect_type, Place
import random
from datetime import datetime
from .utils import admin_verify, user_verify, sensor_verify
from .errors import UserError, CollectError
import time
from ..utils import Redis

PASS_TIME=10

@api.route('/views/sensor/number', methods=['GET'])
def sensor_number():
    data=0
    now_time=time.time()
    try:
        col = Collector.query.filter_by(isonline=True)
        data=col.count()
        if(data > 0):
            for c in col:
                da=c.run_time
                t=time.mktime(da.timetuple())  
                if(t+PASS_TIME < now_time):
                    data-=1
                    Redis.lpush(rredis,"info_list",{"place":c.collector_place.name,"time":now_time,"sensor":c.name,"info":"设备离线","code":300});
                    print(":设备离线")
                    c.isonline=False
                    db.session.add(c)
                    
            db.session.commit() 
        code, msg = 200, 'OK'
    except Exception as e:
        print("Error:"+e.__str__())
        code, msg = 403, "无数据"
        db.session.rollback()
    return jsonify({"code": code,
                    "msg": msg,
                    "data": {
                        "data":data,
                        "time":time.time()
                    }
                    })


@api.route('/views/place/number', methods=['GET'])
def place_number():
    data=0
    try:
        pl = Place.query.all()
        data=len(pl)
      
        code, msg = 200, 'OK'
    except Exception as e:
        print("Error:"+e.__str__())
        code, msg = 403, "无数据"
    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    })
        


@api.route('/views/global_status', methods=['GET'])
def glo_info():
    sen_num,online_num,place_num,now_time=0,0,0,time.time()
    try:
        place_num=len(Place.query.all())
        sen_num =len(Collector.query.all())
        col = Collector.query.filter_by(isonline=True)
        online_num=col.count()
        # online_num=int(sen_num)
        if(online_num > 0):
            for c in col:
                da=c.run_time
                t=time.mktime(da.timetuple())  
                if(t+PASS_TIME < now_time):
                    online_num-=1
                    c.isonline=False
                    Redis.lpush(rredis,"info_list",{"place":c.collector_place.name,"time":now_time,"sensor":c.name,"info":"设备离线","code":300});
                    print(":设备离线")
                    db.session.add(c)
                    
            db.session.commit() 
        code, msg = 200, 'OK'
    except Exception as e:
        print("Error:"+e.__str__())
        code, msg = 403, "无数据"
        db.session.rollback()
    return jsonify({"code": code,
                    "msg": msg,
                    "data": {"sen_num":sen_num,
                            "online_num":online_num,
                            "place_num":place_num
                            }
                    })

@api.route('/views/info_que', methods=['GET'])
def info_que():
    code,msg,data=200,"OK",Redis.lrange(rredis,"info_list",0,-1) 

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data
                    })