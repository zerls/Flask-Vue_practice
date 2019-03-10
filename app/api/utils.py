from ..models import User, Role,Collector

from flask import request,jsonify
from .errors import UserError,CollectError
import re

def admin_verify(func):
    def deco(func):
        def wrapper(*args, **kwargs):
            try:       
                # token=request.args.get('token')
                token=request.headers.get('Authorization')
                admin_user = User.verify_auth_token(token) 
                # print(admin_user.is_administrator()) 
                if admin_user is not None and admin_user.is_administrator():
                    return    func(*args,**kwargs)
                raise UserError('admin verify false')
            except Exception as e:
                print("ERROR: "+e.__str__())
                raise e
                return jsonify({"code": 401,
                        "msg": "auto verift false"})     
        wrapper.__name__ = func.__name__      
        return wrapper
    return deco if not func else deco(func)

def user_verify(func):
    def wrapper(*args, **kwargs):
        try:       
            token=request.headers.get('Authorization')
            # token=request.args.get('token')
            if token:
                user = User.verify_auth_token(token)
                if user is not None:
                    return    func(*args,**kwargs)
            raise UserError('user verify false')
        except Exception as e:
            print("ERROR: "+e.__str__())
            return jsonify({"code": 401,
                    "msg": "auto verift false"})     
    wrapper.__name__ = func.__name__ 
    return wrapper

def sensor_verify(func):
    def wrapper(*args, **kwargs):
        try:       
            token=request.headers.get('Authorization')
            print("设备型号："+request.headers.get('User-Agent'))
            if token:
                col = Collector.verify_auth_token(token)
                if col is not None:
                    return    func(col,*args,**kwargs)
            raise CollectError('Collector verify false')
        except Exception as e:
            print("ERROR: "+e.__str__())
            return jsonify({"code": 401,
                    "msg": "auto verift false"})     
    wrapper.__name__ = func.__name__ 
    return wrapper

def float_verify(y):
    find_float = lambda x: re.search("10|(\d(\.\d{0,2})?)",x)  .group()
    y=str(y)
    if not y==find_float(y):
        raise ValueError("数值有效范围: (0.00,10.00)")


def name_verify(y):
    find_name = lambda x: re.search("^[a-zA-Z0-9_-]{4,16}",x)  .group()
    # y=str(y)
    try:
        if not y==find_name(y):
            raise ValueError("无效命名")
    except AttributeError:
        raise ValueError("无效命名")

def z_name_verify(y):
    find_name = lambda x: re.search("^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9]){2,10}",x)  .group()
    # y=str(y)
    try:
        if not y==find_name(y):
            raise ValueError("无效命名")
    except AttributeError:
        raise ValueError("无效命名")
    