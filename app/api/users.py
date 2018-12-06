from flask import jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import User, Role
import random
from datetime import datetime
from .utils import admin_verify, user_verify

@api.route('/user/action/token',methods=['GET'])
@user_verify
def user_token():
    return jsonify({"code": 200,
                    "msg": 'OK'})

@api.route('/user/action/login', methods=['POST'])
def login():
    
    code,token, access_time, msg = 401,  "",  0, "账号或密码错误"
    data=request.get_data()
    print(data)
    if request.json:
        username = request.json["username"]
        password = request.json["password"]
        print(username=="")
        print(password=="")
        if username == "" or password == "":
            msg="账号或密码不能为空"    
        user = User.query.filter_by(username=username).first()
        # if user is not None and user.confirmed==False and user.verify_password(password):
        if user is not None and user.verify_password(password):
            access_time = 3600
            token = user.generate_auth_token(expiration=access_time)
            code,msg = 200,"OK"

    return jsonify({"code": code,
                    "token": token,
                    "access_token_time": access_time,
                    "msg": msg}),code



@api.route('/user/action/uptoken', methods=['GET'])
def uptoken():
    try:
        token = request.args.get('token')
        user = User.verify_auth_token(token)
        code = 200
        time = 600
        msg = 'OK'
        token = user.generate_auth_token(
            expiration=time)
    except:
        code, token, time, msg = 403, "", 0, "请求失败"
    return jsonify({"code": code,
                    "token": token,
                    "token-time": time,
                    "msg": msg})


# //用户密码修改
# /api/version/user/action/password?token=_ [PATCH]
@api.route('/user/action/password', methods=['PATCH'])
@admin_verify
def password():
    try:
        user_id = request.json["user_id"]
        user = User.query.filter_by(id=user_id).first()
        user.password = request.json['password']
        db.session.add(user)
        db.session.commit()
        code = 200
        msg = '退出成功'
    except:
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})

# //用户权限修改
# /api/version/user/permission [PATCH]
@api.route('user/permission',methods=['PATCH'])
@admin_verify
def user_premiss():
    try:
        json=request.json
        user = User.query.filter_by(id=json['user_id']).first()
        user.role.add_permission(16)
        db.session.add(user)
        db.session.commit()
        code,msg=200,"修改成功"
    except :
        code,msg=404,'无数据'
    return jsonify({"code": code,
                    "msg": msg,
    })

# //用户信息修改
# /api/version/user/{int:user.id} [PATCH]
@api.route('/user',methods=['PATCH'])
@admin_verify
def pat_user():
    try:
        json = request.json
        name=json['update']['name']
        user = User.query.filter_by(id=json['id']).first()
        if name: 
            user.name=name
            db.session.add(user)
            db.session.commit()
            code, msg = 200, 'OK'
        else:
            code, msg = 403, '无效提交'
    except:
        db.session.rollback()
        code, msg = 404, "修改失败"
    return jsonify({"code": code,
                    "msg": msg})

# //用户查找
# /api/version/user [GET]
@api.route('/user', methods=['GET'])
@admin_verify
def user_find():
    role = request.args.get('role')
    uid = request.args.get('id')
    number= request.args.get('number')
    code,msg = 200,"获取成功"
    if role:
        role = Role.query.filter_by(name=role).first()
        if number:
            users = User.query.filter_by(role=role).limit(number)
            data=[]
            for user in users:
                da={"id":user.id,"name":user.name}
                data.append(da)
        else:
            user = User.query.filter_by(role=role).first()
            data=[{"id":user.id,"name":user.name}]
    elif uid:
        user = User.query.filter_by(id=uid).first()
        data=[{"id":user.id,"name":user.name}]
    else:
        code,msg,data = 404,"无数据",[]

    return jsonify({"code": code,
                    "msg": msg,
                    "data":data,
    })


# //用户删除
@api.route('/user', methods=['DELETE'])
@admin_verify
def delete():
    try:
        user_id = request.json["user_id"]
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        code = 200
        msg = '退出成功'
    except:
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})


# //用户添加
# /api/version/user [POST]
@api.route('/user', methods=['POST'])
@admin_verify
def add_user():
    try:
        json = request.json
        code = 200
        msg = 'OK'
        user_role = Role.query.filter_by(name=json['role']).first()
        user = User(username=json['name'], role=user_role,
                    password=json['password'], name=json['name'])
        db.session.add(user)
        db.session.commit()
    except:
        code, msg = 404, "无数据"
    return jsonify({"code": code,
                    "msg": msg})
