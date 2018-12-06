from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import Collector, Collect_state, Collect_type, Place
import random
from datetime import datetime
from .utils import admin_verify, user_verify, sensor_verify
from .errors import UserError, CollectError

# //设备通信token获取
@api.route('/sensor/action/token', methods=['POST'])
def s_token():
    code, token, token_time, msg = 401, "",  0, "登录失败"
    if request.json:
        name = request.json["name"]
        tokenn = request.json["token"]
        col = Collector.query.filter_by(name=name).first()
        if col is not None and col.verify_token(tokenn):
            token_time = 36000
            token = col.generate_auth_token(expiration=token_time)
            msg = ""
            code = 200

    return jsonify({"code": code,
                    "token": token,
                    "token_time": token_time,
                    "msg": msg})

# //状态反馈&控制
# /api/version/sensor/action?token=_ [GET]


@api.route('/sensor/action', methods=['GET'])
@sensor_verify
def act_sensor(col):
    # TODO
    try:
        state = request.args.get('code')
        timestamp = request.args.get('run_time')
        s = Collect_state.query.filter_by(id=state).first()
        time = datetime.fromtimestamp(timestamp)
        col.collector_state = s
        col.run_time = time
        db.session.add(col)
        db.session.commit()
        code, msg = 200, 'OK'
    except:
        db.session.rollback()
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "data": {
                        "order-code": "",
                        "order-content": "",
                    },
                    "msg": msg})

# //设备删除
@api.route('/place', methods=['DELETE'])
@admin_verify
def del_sensor():
    try:
        sensor = request.args.get('sensor')
        s = Collector.query.filter_by(name=sensor).first()
        db.session.delete(s)
        db.session.commit()
        code, msg = 200, 'OK'
    except:
        db.session.rollback()
        code, msg = 404, "数据不存在"
    return jsonify({"code": code,
                    "msg": msg})


# # //设备删除
# # /api/version/sensor?token=_ [DELETE]
# @api.route('/sensor', methods=['DELETE'])
# @admin_verify
# def del_sensor():
#     try:
#         data = request.json["data"]
#         for d in data:
#             sensor_id = d["sensor_id"]
#             sensor = Collector.query.filter_by(id=sensor_id).first()
#             if sensor is None:
#                 continue
#             db.session.delete(sensor)
#         db.session.commit()
#         code = 200
#         msg = '删除成功'
#     except:
#         db.session.rollback()
#         code, msg = 404, "删除失败"
#     return jsonify({"code": code,
#                     "msg": msg})

# //设备添加
# /api/version/sensor?token=_[POST]


@api.route('/sensor', methods=['POST'])
@admin_verify
def add_sensor():
    try:
        json = request.json
        type = Collect_type.query.filter_by(name=json['type']).first()
        place = Place.query.filter_by(name=json['place']).first()
        state = Collect_state.query.filter_by(id=json['state']).first()
        if type and place and state:
            col = Collector(name=json['name'], collector_type=type, collector_place=place,
                            collector_state=state)
        db.session.add(col)
        db.session.commit()
        code, msg = 200, 'OK'
    except:
        db.session.rollback()
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})

# 设备信息修改  PATCH
# /api/version/sensor?token=_ [PATCH]
@api.route('/sensor', methods=['PATCH'])
@admin_verify
def pat_sensor():
    try:
        json = request.json
        place = Place.query.filter_by(name=json['place']).first()
        col = Collector.query.filter_by(id=json['id']).first()
        if place:
            col.collector_place = place

        db.session.add(col)
        db.session.commit()

        code, msg = 200, 'OK'
    except Exception as e:
        print("Error:"+e.__str__())
        db.session.rollback()
        code, msg = 403, "参数错误"
    return jsonify({"code": code,
                    "msg": msg})

    # //设备查找
    # /api/version/sensor?token=_ [GET]

@api.route('/sensor', methods=['GET'])
@admin_verify
def find_sensor():
    try:
        state = request.args.get('state')
        place = request.args.get('place')
        uid = request.args.get('sensor_id')
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        if not offset:
            offset = 0
        if not limit:
            limit = 1
        code, msg,data = 200, "获取成功",""

        if place or state:
            if place and not state:
                p = Collector.query.filter_by(name=place).first()
                cols = Collector.query.filter_by(
                    collector_place=p).offset(offset).limit(limit)
            if state and not place:
                s = Collect_state.query.filter_by(name=state).first()
                cols = Collector.query.filter_by(
                    collector_state=s).offset(offset).limit(limit)
            if place and state:
                p = Place.query.filter_by(name=place).first()
                s = Collect_state.query.filter_by(name=state).first()
                cols = Collector.query.filter_by(
                    collector_place=p, collector_state=s).offset(offset).limit(limit)

            data = []
            for col in cols:
                da = {"id": col.id, "name": col.name, "type": col.type,
                      "place": col.place, "state": col.state, "run_time": col.run_time}
                data.append(da)

        elif uid:
            col = Collector.query.filter_by(id=uid).first()
            data = [{"id": col.id, "name": col.name, "type": col.type,
                     "place": col.place, "state": col.state, "run_time": col.run_time}]
        elif limit:
            cols = Collector.query.offset(offset).limit(limit)
            data = []
            for col in cols:
                da = {"id": col.id, "name": col.name, "type": col.collector_type.name,
                      "place": col.collector_place.name, "state": col.collector_state.name, "run_time": col.run_time,"token":col.token}
                if da['run_time'] is None:
                    da['run_time']=""
                print(da)
                data.append(da)
        else:
            code, msg, data = 403, "参数错误", []
        
    except Exception as e:
        print(data)
        # print("ERROR: "+e.__str__())
        code, msg, data = 404, "无数据", []

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    })
