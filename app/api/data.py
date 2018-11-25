from datetime import datetime

from flask import current_app, jsonify, request, url_for

from . import api
from .. import db
from ..models import Place,Data,Data_type
from .utils import admin_verify, user_verify,sensor_verify


# //设备采集数据 
# /api/version/data [POST]
@api.route('/data', methods=['POST'])
@sensor_verify
def add_data(col):
    try:
        json = request.json
        place=Place.query.filter_by(name=json['data']['place']).first()
        type=Data_type.filter_by(name=json['data']['type']).first()
        context=json['data']['context']
        d=Data(context=context,data_type=type,data_place=place)
        db.session.add(d)
        db.session.commit()
        code,msg = 200,'OK'
    #TODO png 
    except:
        db.session.rollback()
        code, msg = 403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})

# //数据删除
# /api/version/data?token=_ [DELETE]            
@api.route('/data', methods=['DELETE'])
@admin_verify
def del_data():
    try:
        code,msg = 200,'OK'
        place = request.json['place']
        time_start=request.json['time_start']
        time_slice=request.json['time_slice']
        data_id=request.json['id']
        place=Place.Place.query.filter_by(name=place).first()
        if data_id:
            d = Data.query.filter_by(id=data_id).first()
            db.session.delete(d)
            db.session.commit()
        elif time_start and place:
            if time_slice is None: time_slice=1
            time=datetime.fromtimestamp(time_start)
            d = db.session.query(Data).filter(Data.time.between(time, time+datetime.timedelta(seconds=time_slice)),data_place=place)
            db.session.delete(d)
            db.session.commit()
        else:
            code, msg = 403, "参数错误"
    except:
        db.session.rollback()
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})


# //数据获取
# /api/version/data/ [GET]  
@api.route('/place', methods=['GET'])
@user_verify
def get_data():
    try:

        place = request.args.get('place')
        offset = request.args.get('offset')
        limit= request.args.get('limit')
        if not offset: offset=0
        if limit:
            ps = Data.query.offset(offset).limit(limit)
            data=[]
            for p in ps:
                da={"name":p.name,"x":p.x,"y":p.y}
                data.append(da)
        elif place:
            p = Place.query.filter_by(name=place).first()
            data=[{"name":p.name,"x":p.x,"y":p.y}]
        else:
            code,msg,data = 403,"参数错误",[]
        
    except :
        code,msg,data = 404,"无数据",[]

    return jsonify({"code": code,
                    "msg": msg,
                    "data":data,
    })

  