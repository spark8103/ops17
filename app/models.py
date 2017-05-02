# coding: utf-8
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from marshmallow import Schema, fields, ValidationError, pre_load


class Permission:
    USER = 0x01
    WRITE_ARTICLES = 0x04
    ADMINISTER = 0x80


# MODELS #####
class Role(db.Model):
    __tablename__ = 'ops_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Department(db.Model):
    __tablename__ = 'ops_departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('ops_departments.id'))
    description = db.Column(db.String(128))

    parent = db.relationship("Department", remote_side=[id, name])
    users = db.relationship('User', backref='department')
    projects = db.relationship('Project', backref='department')

    def __repr__(self):
        return '<Department %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'ops_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64))
    mobile = db.Column(db.String(11))
    department_id = db.Column(db.Integer, db.ForeignKey('ops_departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    allow_login = db.Column(db.Boolean, default=False, index=True)
    type = db.Column(db.String(32), index=True, default="user")
    password_hash = db.Column(db.String(128))

    pm = db.relationship('Project',
                         backref=db.backref('pm', lazy='joined'), lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['OPS_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
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

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'email': self.email,
            'mobile': self.mobile,
            'department': self.department.name,
            'type': self.type,
            'member_since': self.member_since,
            'last_seen': self.last_seen
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return "User(id='%s')" % self.id


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Idc(db.Model):
    __tablename__ = 'ops_idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    description = db.Column(db.String(256))

    idc = db.relationship('Server',
                          backref=db.backref('idc', lazy='joined'), lazy='dynamic')
    environments = db.relationship('Environment', backref='idc')

    def __repr__(self):
        return '<Idc %r>' % self.name


class Server(db.Model):
    __tablename__ = 'ops_servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)   # server name
    idc_id = db.Column(db.Integer, db.ForeignKey('ops_idcs.id'), index=True)  # idc info
    rack = db.Column(db.String(64))  # rack info
    private_ip = db.Column(db.String(128))  # private_ip
    public_ip = db.Column(db.String(128))  # public_ip
    category = db.Column(db.String(128), index=True)  # 大数据 征信
    env = db.Column(db.String(64), index=True)  # prd stg dev qa
    type = db.Column(db.String(128))  # server vserver
    status = db.Column(db.String(128))  # 在线 备用 维修
    description = db.Column(db.String(256))   # 备注说明

    def __repr__(self):
        return '<Server %r>' % self.name


class Software(db.Model):
    __tablename__ = 'ops_software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    version = db.Column(db.String(64), unique=True, index=True)

    modules = db.relationship('Module',
                         backref=db.backref('software', lazy='joined'), lazy='dynamic')

    @staticmethod
    def insert_softwares():
        softwares = {
            'es-tomcat': 'tomcat_7.0.68',
            'es-nginx': 'nginx_1.8.1',
            'es-nginx10': 'nginx_1.10.2',
            'es-python': 'python_2.7.11',
            'es-jdk7': 'jdk1.7.0_67',
            'es-jdk8': 'jdk1.8.0_77',
            'es-haproxy': 'haproxy_1.6.4',
            'bd-zabbix-agentd': 'zabbix-agentd_3.0.4',
            'es-tomcatctl': 'tomcatctl',
            'glusterfs': 'glusterfs_3.7.11',
            'tinyproxy': 'tinyproxy_1.8.3',
            'es-kettle': 'kettle_2.3.3',
        }
        for s in softwares:
            software = Software.query.filter_by(name=s).first()
            if software is None:
                software = Software(name=s)
            software.version = softwares[s]
            db.session.add(software)
        db.session.commit()

    def __repr__(self):
        return '<Software %r>' % self.name


class Project(db.Model):
    __tablename__ = 'ops_projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('ops_departments.id'))
    pm_id = db.Column(db.Integer, db.ForeignKey('ops_users.id'))
    sla = db.Column(db.String(32))
    check_point = db.Column(db.String(64))
    description = db.Column(db.String(128))

    project = db.relationship('Module',
                         backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return '<Project %r>' % self.name


class Module(db.Model):
    __tablename__ = 'ops_modules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('ops_projects.id'))
    svn = db.Column(db.String(128))
    parent_id = db.Column(db.Integer, db.ForeignKey('ops_modules.id'))
    dev_id = db.Column(db.Integer, db.ForeignKey('ops_users.id'))
    qa_id = db.Column(db.Integer, db.ForeignKey('ops_users.id'))
    ops_id = db.Column(db.Integer, db.ForeignKey('ops_users.id'))
    software_id = db.Column(db.Integer, db.ForeignKey('ops_software.id'))
    description = db.Column(db.String(128))

    parent = db.relationship("Module", remote_side=[id, name])
    dev = db.relationship('User', foreign_keys=[dev_id])
    qa = db.relationship('User', foreign_keys=[qa_id])
    ops = db.relationship('User', foreign_keys=[ops_id])
    module = db.relationship('Environment',
                              backref=db.backref('module', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return '<Module %r>' % self.name


class Environment(db.Model):
    __tablename__ = 'ops_environments'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('ops_modules.id'))
    env = db.Column(db.String(32))
    idc_id = db.Column(db.Integer, db.ForeignKey('ops_idcs.id'))
    check_point1 = db.Column(db.String(128))
    check_point2 = db.Column(db.String(128))
    check_point3 = db.Column(db.String(128))
    deploy_path = db.Column(db.String(128))
    server_ip = db.Column(db.String(128))
    online_since = db.Column(db.DateTime(), default=datetime.utcnow)
    domain = db.Column(db.String(64))

    def __repr__(self):
        return '<Environment %r>' % self.name

# SCHEMAS #####


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    parent = fields.Nested('self', only=["id", "name"])
    description = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    mobile = fields.Str()
    department = fields.Nested(DepartmentSchema, only=["id", "name"])
    role = fields.Nested(RoleSchema, only=["id", "name"])
    allow_login = fields.Boolean()
    type = fields.Str()
    member_since = fields.DateTime('%Y-%m-%d %H:%M:%S')
    last_seen = fields.DateTime('%Y-%m-%d %H:%M:%S')


class IdcSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()


class ServerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    idc = fields.Nested(IdcSchema, only=["id", "name"])
    rack = fields.Str()
    private_ip = fields.Str()
    public_ip = fields.Str()
    category = fields.Str()
    env = fields.Str()
    type = fields.Str()
    status = fields.Str()
    description = fields.Str()


class SoftwareSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    version = fields.Str()


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    department = fields.Nested(DepartmentSchema, only=["id", "name"])
    pm = fields.Nested(UserSchema, only=["id", "username"])
    sla = fields.Str()
    check_point = fields.Str()
    description = fields.Str()


class ModuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    project = fields.Nested(ProjectSchema, only=["id", "name"])
    svn = fields.Str()
    parent = fields.Nested('self', only=["id", "name"])
    dev = fields.Nested(UserSchema, only=["id", "username"])
    qa = fields.Nested(UserSchema, only=["id", "username"])
    ops = fields.Nested(UserSchema, only=["id", "username"])
    software = fields.Nested(SoftwareSchema, only=["id", "version"])
    description = fields.Str()


class EnvironmentSchema(Schema):
    id = fields.Int(dump_only=True)
    module = fields.Nested(ModuleSchema, only=["id", "name"])
    idc = fields.Nested(IdcSchema, only=["id", "name"])
    env = fields.Str()
    check_point1 = fields.Str()
    check_point2 = fields.Str()
    check_point3 = fields.Str()
    deploy_path = fields.Str()
    server_ip = fields.Str()
    online_since = fields.Str('%Y-%m-%d %H:%M:%S')
    domain = fields.Str()