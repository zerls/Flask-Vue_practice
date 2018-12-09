from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_from_directory, current_app,Response)
from flask_sqlalchemy import SQLAlchemy
from . import main
from .. import db
from ..models import User, Role, Place, Data, Data_type


@main.route('/test', methods=['GET'])
def test():
    user = User.query.filter_by(username="alicse").first()
    if user is None:
        name = 'sss'
    else:
        name = 'alic'

    DEV = current_app.config['DEV']

    return render_template('test.html',
                           name=name, dev=DEV)


@main.route('/', methods=['GET'])
def home_of_no_variable_get():
    # user = User.query.filter_by(username="alicse").first()
    # if user is None:
    #     name = 'sss'
    # else:
    #     name = 'alic'

    # DEV=current_app.config['DEV']

    # return render_template('test.html',
    #     name=name,dev=DEV)
    return render_template('index.html')
    # return redirect('http://localhost:8080/__webpack_hmr')


@main.route('/__webpack_hmr')
def npm():
    return redirect('http://localhost:8080/__webpack_hmr')


@main.route('/about.js')
def npsm():
    return redirect('http://localhost:8080/about.js')


@main.route('/fonts/<file>')
def fonts(file):
    return redirect('/static/fonts/'+file)

# @main.route('/fonts/element-icons.2fad952a.woff')
# def fonts():
#     return redirect('http://localhost:8080/fonts/element-icons.2fad952a.woff')

# @main.route('/fonts/element-icons.6f0a7632.ttf')
# def fonts2():
#     return redirect('http://localhost:8080/fonts/element-icons.6f0a7632.ttf')


@main.route('/api/v0/name', methods=['POST'])
def hasname():
    if request.json:
        name = request.json['name']
        user = User.query.filter_by(username=name).first()
        if user is None:
            hasname = 'No'
        else:
            hasname = 'Yes'
    return jsonify({'hasname': hasname})
    # return jsonify({'hasname': user.password_hash})


@main.route('/api/v0/addname', methods=['POST'])
def addname():
    if request.json:
        name = request.json['name']
        user_role = Role.query.filter_by(name="User").first()
        user = User(username=name, role=user_role)
        # user_lux = User(username='lux',name="lux", role=user_role,password='123456')
        # db.session.add(user_lux)
        db.session.add(user)
        db.session.commit()
    return jsonify({'static': "Ok"})


@main.route('/api/v0/delname', methods=['POST'])
def delname():
    if request.json:
        name = request.json['name']
        user = User.query.filter_by(username=name).first()
        if user is None:
            static = 'No this people'
        else:
            static = 'del Now'
            db.session.delete(user)
    return jsonify({'static': static})


@main.route('/api/v0/listname', methods=['POST'])
def listname():
    if request.json:
        user_role = Role.query.filter_by(name="User").first()
        user = User.query.filter_by(role=user_role).all()
        users = []
        for u in user:
            users.append(u.username)
    return jsonify({'static': users})


@main.route('/api/v0/listUserInfo', methods=['POST'])
def listUser_info():
    if request.json:
        name = request.json['name']
        user = User.query.filter_by(username=name).first()

    return jsonify({'static': user.info()})


@main.route('/api/v0/Place_info', methods=['POST'])
def Place_info():
    if request.json:
        name = request.json['place']
        p = Place.query.filter_by(name=name).first()

    return jsonify({'static': p.info()})


@main.route('/api/v0/listPlace', methods=['POST'])
def listPlace():
    if request.json:
        ps = Place.query.all()
        pl = []
        for p in ps:
            pl.append(p.name)
    return jsonify({'static': pl})


@main.route('/api/v0/data', methods=['GET'])
def get_data():
    if request.json:
        ps = Data.query.all()
        pl = []
        for p in ps:
            info = {'id': p.id, 'context': p.context, 'type': p.data_type,'place':p.data_place}
            pl.append(info)
    return jsonify({pl})


# import  cv2

# class VideoCamera(object):
#     def __init__(self):
#         # 通过opencv获取实时视频流
#         self.video = cv2.VideoCapture(0) 
    
#     def __del__(self):
#         self.video.release()
    
#     def get_frame(self):
#         success, image = self.video.read()
#         # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @main.route('/video_feed')  # 这个地址返回视频流响应
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')  