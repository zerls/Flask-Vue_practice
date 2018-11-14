from datetime import datetime

from flask import current_app, jsonify, request, url_for

from . import api
from .. import db
from ..models import Place
from .utils import admin_verify, user_verify


# //地点添加
# /api/version/place/[POST]
@api.route('/place', methods=['POST'])
@admin_verify
def add_place():

    try:
        json = request.json['data']
        p=Place(name=json['name'],x=json['x'],y=json['y'])
        db.session.add(p)
        db.session.commit()
        code,msg = 200,'OK'
    except:
        db.session.rollback()
        code, msg = 403, "添加失败"
    return jsonify({"code": code,
                    "msg": msg})

# //地点删除
# /api/version/place/ [DELETE]                   
@api.route('/place', methods=['DELETE'])
@admin_verify
def del_place():
    try:
        place = request.json['place']
        p = Place.query.filter_by(name=place).first()
        print(p)
        db.session.delete(p)
        db.session.commit()
        code,msg = 200,'OK'
    except:
        db.session.rollback()
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})

# //地点信息修改
# /api/version/place [PATCH]
@api.route('/place', methods=['PATCH'])
@admin_verify
def pat_place():
    try:
        place = request.json['place']
        p = Place.query.filter_by(name=place).first()
        p.name=request.json['name']
        p.x=request.json['x']
        p.y=request.json['y']
        db.session.add(p)
        db.session.commit()
        code,msg = 200,'OK'
    except:
        db.session.rollback()
        code, msg = 403, "修改失败"
    return jsonify({"code": code,
                    "msg": msg})



@api.route('/place', methods=['GET'])
@user_verify
def place_find():
    try:
        code,msg = 200,"获取成功"

        place = request.args.get('place')
        offset = request.args.get('offset')
        limit= request.args.get('limit')
        if not offset: offset=0
        if limit:
            ps = Place.query.offset(offset).limit(limit)
            data=[]
            for p in ps:
                da={"name":p.name,"x":p.x,"y":p.y}
                data.append(da)
        elif place:
            p = Place.query.filter_by(name=place).first()
            data=[{"name":p.name,"x":p.x,"y":p.y}]
        else:
            code,msg = 403,"参数错误"
        
    except :
        code,msg,data = 404,"无数据",[]

    return jsonify({"code": code,
                    "msg": msg,
                    "data":data,
    })
