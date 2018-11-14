from ..models import User, Role
from flask import request,jsonify
from .error import UserError


def admin_verify(func):
    def deco(func):
        def wrapper(*args, **kwargs):
            try:       
                token=request.args.get('token')
                admin_user = User.verify_auth_token(token) 
                # print(admin_user.is_administrator()) 
                if admin_user is not None and admin_user.is_administrator():
                    return    func(*args,**kwargs)
                raise UserError('admin verify false')
            except:
                return jsonify({"code": 403,
                        "msg": 'admin verify false'})     
        wrapper.__name__ = func.__name__      
        return wrapper
    return deco if not func else deco(func)

def user_verify(func):
    def wrapper(*args, **kwargs):
        try:       
            token=request.args.get('token')
            if token:
                user = User.verify_auth_token(token)
                if user is not None:
                    return    func(*args,**kwargs)
            raise UserError('user verify false')
        except:
            return jsonify({"code": 403,
                    "msg": 'user verify false'})     
    wrapper.__name__ = func.__name__ 
    return wrapper