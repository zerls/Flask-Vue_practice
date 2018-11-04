# from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
class Permission:
    CREATE = 1
    DELETE =2
    READ = 4
    WRITE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ],
            'Adminr': [Permission.CREATE, Permission.DELETE,
                              Permission.WRITE, Permission.READ,
                              Permission.ADMIN],
            'Sensor': [Permission.WRITE],

        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer('ha&rg%fhuk@riFg', expiration)
        # s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer('ha&rg%fhuk@riFg')
        # s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer('ha&rg%fhuk@riFg', expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer('ha&rg%fhuk@riFg')
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def generate_auth_token(self, expiration):
        s = Serializer(['ha&rg%fhuk@riFg'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(['ha&rg%fhuk@riFg'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    collectors = db.relationship('Collector', backref='collector_place', lazy='dynamic')
    datas = db.relationship('Data', backref='data_place', lazy='dynamic')
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    
    def __init__(self, **kwargs):
        super(Place, self).__init__(**kwargs)
    
    #TODO

    def reset_site(self):
        pass

    @property
    def site(self):
        pass

    def __repr__(self):
        return '<Place %r>' % self.name


class Data_type(db.Model):
    __tablename__ = 'data_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    datas = db.relationship('Data', backref='data_type', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Data_type, self).__init__(**kwargs)

    def __repr__(self):
        return '<Data_type %r>' % self.name

class Collect_state(db.Model):
    __tablename__ = 'collect_states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    collectors = db.relationship('Collector', backref='collector_state', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Collect_state, self).__init__(**kwargs)

    def __repr__(self):
        return '<Collect_state %r>' % self.name


class Collector(db.Model):
    __tablename__ = 'collectors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    collector_type = db.Column(db.String(64), unique=False)
    state_describe = db.Column(db.String(64), unique=False)
    run_time = db.Column(db.DateTime)

    place_id = db.Column(db.Integer, db.ForeignKey('places.id')) 
    state_id = db.Column(db.Integer, db.ForeignKey('collect_states.id')) 

    datas = db.relationship('Data', backref='data_collector', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Collector, self).__init__(**kwargs)

    #TODO

    def __repr__(self):
        return '<Collector %r>' % self.name


class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    collector_type = db.Column(db.String(64), unique=False)
    content = db.Column(db.Text(128), unique=False)
    time = db.Column(db.DateTime)
    is_collect = db.Column(db.Boolean)

    place_id = db.Column(db.Integer, db.ForeignKey('places.id')) 
    data_type_id = db.Column(db.Integer, db.ForeignKey('data_types.id'))
    collector_id = db.Column(db.Integer, db.ForeignKey('collectors.id'))  

    def __init__(self, **kwargs):
        super(Data, self).__init__(**kwargs)
        if self.is_collect == None:
            self.is_collect = False

    def __repr__(self):
        return '<Data %r>' % self.content


