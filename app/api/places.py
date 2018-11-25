from datetime import datetime

from flask import current_app, jsonify, request, url_for

from . import api
from .. import db
from ..models import Place
from .utils import admin_verify, user_verify, float_verify, z_name_verify


# //地点添加
# /api/version/place/[POST]
@api.route('/place', methods=['POST'])
@admin_verify
def add_place():

    try:
        json = request.json['data']
        x = json['x']
        y = json['y']
        z_name_verify(json['name'])
        float_verify(x)
        float_verify(y)
        p = Place(name=json['name'], x=x, y=y)
        db.session.add(p)
        db.session.commit()
        code, msg, id = 200, 'OK', p.id
    except ValueError as e:
        db.session.rollback()
        code, msg, id = 403, e.__str__(), ""
    except:
        db.session.rollback()
        code, msg, id = 403, "添加失败", ""
    # code=403
    return jsonify({"code": code,
                    "id": id,
                    "msg": msg})

# //地点删除
# /api/version/place/ [DELETE]


@api.route('/place', methods=['DELETE'])
@admin_verify
def del_place():
    try:
        place = request.args.get('place')
        p = Place.query.filter_by(name=place).first()
        # print(p)
        db.session.delete(p)
        db.session.commit()
        code, msg = 200, 'OK'
    except:
        db.session.rollback()
        code, msg = 404, "数据不存在"
    return jsonify({"code": code,
                    "msg": msg})

# //地点信息修改
# /api/version/place [PATCH]


@api.route('/place', methods=['PATCH'])
@admin_verify
def pat_place():
    try:
        uid = request.json['id']
        p = Place.query.filter_by(id=uid).first()
        p.name = request.json['name']
        p.x = request.json['x']
        p.y = request.json['y']
        db.session.add(p)
        db.session.commit()
        code, msg = 200, 'OK'
    except:
        db.session.rollback()
        code, msg = 403, "修改失败"
    return jsonify({"code": code,
                    "msg": msg})


@api.route('/place', methods=['GET'])
@user_verify
def place_find():
    try:
        code, msg = 200, "获取成功"
        lists = request.args.get('list')
        place = request.args.get('place')
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        if not offset:
            offset = 0
        if limit:
            ps = Place.query.offset(offset).limit(limit)
            data = []
            for p in ps:
                da = {"id": p.id, "name": p.name, "x": p.x, "y": p.y}
                data.append(da)
        elif place:
            p = Place.query.filter_by(name=place).first()
            data = [{"id": p.id, "name": p.name, "x": p.x, "y": p.y}]
        else:
            code, msg, data = 403, "参数错误", []

    except:
        code, msg, data = 404, "无数据", []

    return jsonify({"code": code,
                    "msg": msg,
                    "data": data,
                    })


@api.route('/place/action/list', methods=['GET'])
@user_verify
def list_Place():
    ps = Place.query.all()
    pl = []
    for p in ps:
        pl.append(p.name)
    code, msg = 200, "获取成功"
    return jsonify({"code": code,"msg": msg,"data": pl,})
