from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_from_directory,current_app)
from flask_sqlalchemy import SQLAlchemy
from . import main
from .. import db
from ..models import User,Role


@main.route('/', methods=['GET'])
def home_of_no_variable_get():
    user = User.query.filter_by(username="alicse").first()
    if user is None:             
        name = 'sss'
    else:           
        name = 'alic' 

    DEV=current_app.config['DEV']
    
    return render_template('test.html',
        name=name,dev=DEV)

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

@main.route('/api/v0/addname', methods=['POST'])
def addname():
    if request.json:
        name = request.json['name']
        user_role = Role.query.filter_by(name="User").first()
        user = User(username=name, role=user_role)
        db.session.add(user) 
        db.session.commit()
    return jsonify({'static':"Ok"})

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
        users=[]
        for u in user:
            users.append(u.username)
    return jsonify({'static': users})