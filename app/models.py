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
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.WRITE_ARTICLES, True),
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
    name = db.Column(db.String(64), unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('ops_departments.id'))
    description = db.Column(db.String(128))

    parent = db.relationship("Department", remote_side=[id, name])

    @staticmethod
    def insert_departments():
        departments = {
            u'管理中心': (0,''),
            u'技术中心': (0, ''),
            u'营销中心': (0, ''),
            u'行政部': (Department.query.filter_by(name=u"管理中心").first(),''),
            u'财务部': (Department.query.filter_by(name=u"管理中心").first(), ''),
            u'运维部': (Department.query.filter_by(name=u"技术中心").first(), ''),
            u'开发部': (Department.query.filter_by(name=u"技术中心").first(), ''),
            u'市场部': (Department.query.filter_by(name=u"营销中心").first(), ''),
            u'活动部': (Department.query.filter_by(name=u"营销中心").first(), ''),
        }
        for r in departments:
            department = Department.query.filter_by(name=r).first()
            if department is None:
                department = Department(name=r)
            if isinstance(departments[r][0], int):
                department.parent_id = departments[r][0]
            else:
                department.parent = departments[r][0]
            department.description = departments[r][1]
            db.session.add(department)
        db.session.commit()

    def __repr__(self):
        return '<Department %r>' % self.name


class Idc(db.Model):
    __tablename__ = 'ops_idcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))

    servers = db.relationship('Server', backref='servers', lazy='dynamic')

    @staticmethod
    def insert_idcs():
        idcs = {
            u'周浦': '',
            u'宛平南路': '',
            u'欧阳路': '',
            u'万国数据中心': '',
            u'Ucloud': '',
        }
        for s in idcs:
            idc = Idc.query.filter_by(name=s).first()
            if idc is None:
                idc = Idc(name=s)
            idc.description = idcs[s]
            db.session.add(idc)
        db.session.commit()

    def __repr__(self):
        return '<Idc %r>' % self.name


class Server(db.Model):
    __tablename__ = 'ops_cmdbs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)   # server name
    idc_id = db.Column(db.Integer, db.ForeignKey('ops_idcs.id'))  # idc info
    rack = db.Column(db.String(64))  # rack info
    private_ip = db.Column(db.String(128))  # private_ip
    public_ip = db.Column(db.String(128))  # public_ip
    category = db.Column(db.String(128))  # 大数据 征信
    env = db.Column(db.String(64))  # prd stg dev qa
    type = db.Column(db.String(128))  # server vserver
    status = db.Column(db.String(128))  # 在线 备用 维修
    description = db.Column(db.String(256))   # 备注说明

    @staticmethod
    def insert_cmdbs():
        servers = {
            u'zp-prd-app-10': (
            Idc.query.filter_by(name=u"周浦").first(), "K1", '10.10.10.10', '', '大数据', "prd", "server", "在线", ""),
            u'zp-prd-app-11': (
            Idc.query.filter_by(name=u"周浦").first(), "K2", '10.10.10.11', '', '大数据', "prd", "server", "在线", ""),
            u'oyl-stg-app-101': (
                Idc.query.filter_by(name=u"欧阳路").first(), "R11", '10.18.23.101', '', '征信', "stg", "server", "在线", ""),
            u'wpn-dev-oracle-21': (
                Idc.query.filter_by(name=u"宛平南路").first(), "A01", '172.16.11.21', '', '大数据', "dev", "vserver", "在线", ""),
            u'wpn-dev-oracle-22': (
                Idc.query.filter_by(name=u"宛平南路").first(), "A01", '172.16.11.22', '', '大数据', "dev", "vserver", "在线", ""),
        }
        for s in servers:
            server = Server.query.filter_by(name=s).first()
            if server is None:
                server = server(name=s)
            server.idc = servers[s][0]
            server.rack = servers[s][1]
            server.private_ip = servers[s][2]
            server.public_ip = servers[s][3]
            server.category = servers[s][4]
            server.env = servers[s][5]
            server.type = servers[s][6]
            server.status = servers[s][7]
            server.description = servers[s][8]
            db.session.add(server)
        db.session.commit()

    def __repr__(self):
        return '<Server %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'ops_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), index=True)
    mobile = db.Column(db.INTEGER, index=True)
    department = db.Column(db.String(32), index=True, default="user")
    role_id = db.Column(db.Integer, db.ForeignKey('ops_roles.id'))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    allow_login = db.Column(db.Boolean, default=False, index=True)
    pm = db.relationship('Project',
                         backref=db.backref('pm', lazy='joined'), lazy='dynamic')
    @staticmethod
    def insert_users():
        users = {
            'admin': ('admin@example.com', 13465245521, "admin", Role.query.filter_by(name="Administrator").first(), 'admin', True),
            'ops1': ('ops1@example.com', 13764110236, "ops", Role.query.filter_by(name="User").first(), 'ops1', False),
            'ops2': ('ops2@example.com', 13764110238, "ops", Role.query.filter_by(name="User").first(), 'ops2', False),
            'dev1': ('dev1@example.com', 13612451124, "dev", Role.query.filter_by(name="User").first(), 'dev1', False),
            'dev2': ('dev2@example.com', 13625412214, "dev", Role.query.filter_by(name="User").first(), 'dev2', False),
            'qa1': ('qa1@example.com', 13112453365, "qa", Role.query.filter_by(name="User").first(), 'qa1', False),
            'qa2': ('qa2@example.com', 13124556847, "qa", Role.query.filter_by(name="User").first(), 'qa2', False),
            'dba1': ('dba1@example.com', 13321542635, "dba", Role.query.filter_by(name="User").first(), 'dba1', False),
            'dba2': ('dba2@example.com', 13214512245, "dba", Role.query.filter_by(name="User").first(), 'dba2', False),
            'user1': ('user1@example.com', 13412115694, "user", Role.query.filter_by(name="User").first(), 'user1', False),
            'user2': ('user2@example.com', 13451489521, "user", Role.query.filter_by(name="User").first(), 'user2', False),
            'user3': ('user3@example.com', 13465218952, "manager", Role.query.filter_by(name="User").first(), 'user3', False),
            'user4': ('user4@example.com', 13462548991, "manager", Role.query.filter_by(name="User").first(), 'user4', False),
        }
        for u in users:
            user = User.query.filter_by(username=u).first()
            if user is None:
                user = User(username=u)
            user.email = users[u][0]
            user.mobile = users[u][1]
            user.department = users[u][2]
            user.role = users[u][3]
            user.password = users[u][4]
            user.allow_login = users[u][5]
            db.session.add(user)
        db.session.commit()

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
            'department': self.department,
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


class Software(db.Model):
    __tablename__ = 'ops_software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    version = db.Column(db.String(64), unique=True, index=True)
    software = db.relationship('Module',
                         backref=db.backref('software', lazy='joined'), lazy='dynamic')

    @staticmethod
    def insert_softwares():
        softwares = {
            'es-tomcat': 'tomcat_7.0.68',
            'es-nginx': 'nginx_1.8.1',
            'es-python': 'python_2.7.11',
            'es-jdk7': 'jdk1.7.0_67',
            'es-jdk8': 'jdk1.8.0_77',
            'es-haproxy': 'haproxy_1.6.4',
            'bd-zabbix-agentd': 'zabbix-agentd_3.0.4',
            'es-tomcatctl': 'tomcatctl',
            'glusterfs': 'glusterfs_3.7.11',
            'tinyproxy': 'tinyproxy_1.8.3',
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


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Project(db.Model):
    __tablename__ = 'ops_projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(32), index=True, default="user")
    pm_id = db.Column(db.Integer, db.ForeignKey('ops_users.id'))
    sla = db.Column(db.String(32))
    check_point = db.Column(db.String(64))
    domain = db.Column(db.String(64))
    description = db.Column(db.String(128))
    project = db.relationship('Module',
                         backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return '<Project %r>' % self.name


class Module(db.Model):
    __tablename__ = 'ops_modules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('ops_projects.id'))
    department = db.Column(db.String(32), index=True)
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
    idc = db.Column(db.String(64))
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


class DepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    parent = fields.Nested('self', only=["id", "name"])
    description = fields.Str()


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


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()


class SoftwareSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    version = fields.Str()


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    department = fields.Str()
    pm = fields.Nested(UserSchema, only=["id", "username"])
    sla = fields.Str()
    check_point = fields.Str()
    domain = fields.Str()
    description = fields.Str()


class ModuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    project = fields.Nested(ProjectSchema, only=["id", "name"])
    department = fields.Str()
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
    idc = fields.Str()
    env = fields.Str()
    check_point1 = fields.Str()
    check_point2 = fields.Str()
    check_point3 = fields.Str()
    deploy_path = fields.Str()
    server_ip = fields.Str()
    online_since = fields.Str()
    domain = fields.Str()