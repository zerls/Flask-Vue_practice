from datetime import datetime, timedelta
import urllib
import time
from flask import current_app, jsonify, request, url_for

from . import api
from .. import db
from ..models import Place, Data, Data_type
from .utils import admin_verify, user_verify, sensor_verify

# //设备采集数据 添加
# /api/version/data [POST]


@api.route('/data', methods=['POST'])
@sensor_verify
def add_data(col):
    try:
        json = request.json
        place = Place.query.filter_by(name=json['data']['place']).first()
        type = Data_type.query.filter_by(name=json['data']['type']).first()
        content = json['data']['content']
        d = Data(content=content, data_type=type,
                 data_place=place, data_collector=col)
        db.session.add(d)
        db.session.commit()
        print(1)
        code, msg = 200, 'OK'
    # TODO png
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg = 403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})


# //数据删除
# /api/version/data?token=_ [DELETE]
@api.route('/data', methods=['DELETE'])
# @admin_verify
def del_data():
    try:
        code, msg = 200, 'OK'
        place = request.json['place']
        types = request.json['type']
        time_start = request.json['time_start']
        time_slice = request.json['time_slice']
        data_id = request.json['id']
        place = Place.query.filter_by(name=place).first()
        types = Data_type.query.filter_by(name=types).first()
        if data_id is not "":
            d = Data.query.filter_by(id=data_id).first()
            db.session.delete(d)
            db.session.commit()
        elif time_start and place:
            if time_slice is None:
                time_slice = 1
            time = datetime.fromtimestamp(int(time_start))
            # d = db.session.query(Data).filter(Data.time.between(time, time+timedelta(seconds=int(time_slice))),
            # data_place=place, data_type=types)
            ds = db.session.query(Data).filter(Data.time.between(
                time, time+timedelta(seconds=int(time_slice))))
            for d in ds:
                db.session.delete(d)
            db.session.commit()
        else:
            code, msg = 403, "参数错误"
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})


# TODO
# //采集数据类型列表
# /api/version/data [GET]  data/type/list
@api.route('/data', methods=['POST'])
# @user_verify
def get_datatype(col):
    try:
        json = request.json
        place = Place.query.filter_by(name=json['data']['place']).first()
        type = Data_type.query.filter_by(name=json['data']['type']).first()
        content = json['data']['content']
        d = Data(content=content, data_type=type,
                 data_place=place, data_collector=col)
        db.session.add(d)
        db.session.commit()
        print(1)
        code, msg = 200, 'OK'
    # TODO png
    except Exception as e:
        print("ERROR: "+e.__str__())
        db.session.rollback()
        code, msg = 403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})


# TODO
# //历史数据获取
# /api/version/data [GET]  data/type/list
@api.route('/data/action/history', methods=['POST'])
# @user_verify
def get_dataHis():
    try:
        json = request.json
        print(request.data)
        place = json['place']
        types = json['type']
        time_start=int(json['sdate'])/1000
        time_slice=int(json['edate'])/1000-time_start

        place = urllib.parse.unquote(place)
        types = urllib.parse.unquote(types)
        p = Place.query.filter_by(name=place).first()
        t = Data_type.query.filter_by(name=types).first()
        if p and t:
            time_ = datetime.fromtimestamp(int(time_start))

            ds = db.session.query(Data).filter(Data.time.between(
                time_, time_+timedelta(seconds=int(time_slice)))).filter_by(data_place=p, data_type=t).order_by(
                Data.id).all()
            data = []
            for d in ds:
                data.append(
                    {"data": d.content, "time": time.mktime(d.time.timetuple())})
            code, msg = 200, 'OK'
            print(data)
        else:
            code, msg, data, times = 404, "无数据", [], ''
    except Exception as e:
        print("ERROR: "+e.__str__())
        code, msg, data, times = 403, "参数错误", [], ''

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
        types = request.args.get('type')
        sdate = request.args.get('sdate')
        edate = request.args.get('edate')
        place = urllib.parse.unquote(place)
        types = urllib.parse.unquote(types)
        p = Place.query.filter_by(name=place).first()
        t = Data_type.query.filter_by(name=types).first()
        if p and t:
            d = Data.query.filter_by(data_place=p, data_type=t).order_by(
                Data.id.desc()).first()
            code, msg, data, times = 200, 'OK', d.content, time.mktime(
                d.time.timetuple())
            print(data)
        else:
            code, msg, data, times = 404, "无数据", [], ''
    except Exception as e:
        print("ERROR: "+e.__str__())
        code, msg, data, times = 403, "参数错误", [], ''

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    "time": times,
                    })
