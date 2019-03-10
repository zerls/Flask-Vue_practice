from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Collector, Collect_state, Collect_type, Place
import random
from datetime import datetime
from .utils import admin_verify, user_verify, sensor_verify
from .errors import UserError, CollectError
import time

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
                if(t+60 < now_time):
                    data-=1
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
                    "data": data,
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
        