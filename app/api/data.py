from datetime import datetime, timedelta
import urllib
import time
from flask import current_app, jsonify, request, url_for
from datetime import datetime, timedelta
from . import api
from .. import db, rredis
from ..models import Place, Data, Data_type,Collector
from ..utils import Redis
from .utils import admin_verify, user_verify, sensor_verify
import cmath
# //设备采集数据 添加
# /api/version/data [POST]


@api.route('/data', methods=['POST'])
@sensor_verify
def add_data(col):

    try:
        json = request.json
        place = Place.query.filter_by(name=json['data']['place']).first()
        types_ = Data_type.query.filter_by(name=json['data']['type']).first()
        content = json['data']['content']
        strkey = str(json['data']['place'])+"::"+str(json['data']['type'])
        val={"data": content, "time": datetime.today(), "data_collector": col.id}
        Redis.zadd(rredis, strkey, val);
        now_time=col.run_time=datetime.today()

        if(col.isonline == False):
            Redis.lpush(rredis,"info_list",{"place":json['data']['place'],"time":time.time(),"sensor":col.name,"info":"设备登录","code":200});
        if(float(content) >100):
            Redis.lpush(rredis,"info_list",{"place":json['data']['place'],"time":time.time(),"sensor":col.name,"info":"数据异常","code":404});
        col.isonline=True
        db.session.add(col)


        strkey=str(json['data']['place'])+"::"+str(json['data']['type']) 
        data_l=Redis.zrange(rredis,strkey,0,10) 
        # if(rredis.zcard(strkey) >= 50):
        if(rredis.zcard(strkey) >= 5):
            data = data_l[rredis.zcard(strkey)-1]
            content=data['data']
            place = Place.query.filter_by(name=json['data']['place']).first()
            types_ = Data_type.query.filter_by(name=json['data']['type']).first()
            col = Collector.query.filter_by(id=data['data_collector']).first()
            print((data['time']))
            d_ = Data(content=content, data_type=types_,data_place=place, data_collector=col,time=data['time'])
            db.session.add(d_)
            rredis.delete(strkey)
            print("redis::OK",strkey)


        db.session.commit()



        code, msg=200, 'OK'
    # TODO png
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg=403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})


# //数据删除
# /api/version/data?token=_ [DELETE]
@api.route('/data', methods = ['DELETE'])
# @admin_verify
def del_data():
    try:
        code, msg=200, 'OK'
        place=request.json['place']
        types=request.json['type']
        time_start=request.json['time_start']
        time_slice=request.json['time_slice']
        data_id=request.json['id']
        place=Place.query.filter_by(name = place).first()
        types=Data_type.query.filter_by(name = types).first()
        if data_id is not "":
            d=Data.query.filter_by(id = data_id).first()
            db.session.delete(d)
            db.session.commit()
        elif time_start and place:
            if time_slice is None:
                time_slice=1
            time=datetime.fromtimestamp(int(time_start))
            # d = db.session.query(Data).filter(Data.time.between(time, time+timedelta(seconds=int(time_slice))),
            # data_place=place, data_type=types)
            ds=db.session.query(Data).filter(Data.time.between(
                time, time+timedelta(seconds=int(time_slice))))
            for d in ds:
                db.session.delete(d)
            db.session.commit()
        else:
            code, msg=403, "参数错误"
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg=404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})


# TODO
# //采集数据类型列表
# /api/version/data [GET]  data/type/list
@api.route('/data', methods = ['POST'])
# @user_verify
def get_datatype(col):
    try:
        json=request.json
        place=Place.query.filter_by(name = json['data']['place']).first()
        type=Data_type.query.filter_by(name = json['data']['type']).first()
        content=json['data']['content']
        d=Data(content = content, data_type = type,
                 data_place = place, data_collector = col)
        db.session.add(d)
        db.session.commit()
        print(1)
        code, msg=200, 'OK'
    # TODO png
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg=403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})


# TODO
# //历史数据获取
# /api/version/data [GET]  data/type/list
@api.route('/data/action/history', methods = ['POST'])
# @user_verify
def get_dataHis():
    try:
        json=request.json
        print(request.data)
        place=json['place']
        types=json['type']
        time_start=int(json['sdate'])/1000
        time_slice=int(json['edate'])/1000-time_start

        place=urllib.parse.unquote(place)
        types=urllib.parse.unquote(types)
        p=Place.query.filter_by(name = place).first()
        t=Data_type.query.filter_by(name = types).first()
        if p and t:
            time_=datetime.fromtimestamp(int(time_start))

            ds=db.session.query(Data).filter(Data.time.between(
                time_, time_+timedelta(seconds=int(time_slice)))).filter_by(data_place = p, data_type = t).order_by(
                Data.id).all()
            data = []
            
            for d in ds:
                data.append(
                    {"data": round(float(d.content), 2), "time": time.mktime(d.time.timetuple())})
            code, msg = 200, 'OK'
            print(data)
        else:
            code, msg, data, times = 404, "无数据", [], ''
        if data==[]:
            code, msg, data, times = 405, "无数据", [], ''
    except Exception as e:
        print("ERROR: "+e.__str__())
        code, msg, data, times = 403, "参数错误", [], ''

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    })



# TODO
# //历史数据获取
# /api/version/data [GET]  data/type/list
@api.route('/data/type/list', methods=['GET'])
# @user_verify
def get_datatype_list():
    code,msg =200,"OK"
    data=[]
    d=Data_type.query.all()
    for ds in d:
        data.append(ds.name);
    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    })


# sdate: 1547395200000
# edate: 1548691200000
# //最近数据获取
# /api/version/data/ [GET]


@api.route('/data/action/last', methods=['GET'])
# @user_verify
def last_data():
    try:
        place = request.args.get('place')
        sdate = request.args.get('sdate')
        edate = request.args.get('edate')
        t = Data_type.query.all()
        data=[]
        nisnew=True
        for ts in t:
            data_=[]
            strkey=str(place)+"::"+str(ts.name) 
            data_l=Redis.zrange(rredis,strkey,0,50) 
            len_=rredis.zcard(strkey)
            if(len_!=0):
                nisnew=False
                na = data_l[len_-1]
                code, msg, data_, times = 200, 'OK', na['data'], time.mktime(na['time'].timetuple())
                data.append(data_)
            print(data)
        if data_==[]:
            code, msg, data, times = 404, "无数据", [], ''
        
        if  nisnew or time.mktime(na['time'].timetuple()) < (time.time()-60):
            data,msg,code=[],"无新数据",405
            print(msg,code)
    except Exception as e:
        print("ERROR: "+e.__str__())
        code, msg, data, times = 405, "无数据", [], ''

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    "time": times,
                    })
