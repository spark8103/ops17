#!/bin/env python
# coding: utf-8

from app import db
from app.models import User, Role, Department, Idc, Server, Software, Project, Module, Environment
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


def department_insert_data():
    departments = {
        u'管理中心': (None,''),
        u'技术中心': (None, ''),
        u'营销中心': (None, ''),
        u'行政部': (Department.query.filter_by(name=u"管理中心").first(),''),
        u'财务部': (Department.query.filter_by(name=u"管理中心").first(), ''),
        u'运维部': (Department.query.filter_by(name=u"技术中心").first(), ''),
        u'DBA部': (Department.query.filter_by(name=u"技术中心").first(), ''),
        u'开发部': (Department.query.filter_by(name=u"技术中心").first(), ''),
        u'测试部': (Department.query.filter_by(name=u"技术中心").first(), ''),
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
    print "Insert department test data."


def user_insert_data():
    users = {
        'admin': ('admin@example.com', 13465245521, Department.query.filter_by(name=u"管理中心").first(),
                  Role.query.filter_by(name="Administrator").first(), 'admin', True, "admin"),
        'ops1': ('ops1@example.com', 13764110236, Department.query.filter_by(name=u"运维部").first(),
                 Role.query.filter_by(name="User").first(), 'ops1', False, "ops"),
        'ops2': ('ops2@example.com', 13764110238, Department.query.filter_by(name=u"运维部").first(),
                 Role.query.filter_by(name="User").first(), 'ops2', False, "ops"),
        'dev1': ('dev1@example.com', 13612451124, Department.query.filter_by(name=u"开发部").first(),
                 Role.query.filter_by(name="User").first(), 'dev1', False, "dev"),
        'dev2': ('dev2@example.com', 13625412214, Department.query.filter_by(name=u"开发部").first(),
                 Role.query.filter_by(name="User").first(), 'dev2', False, "dev"),
        'qa1': ('qa1@example.com', 13112453365, Department.query.filter_by(name=u"测试部").first(),
                Role.query.filter_by(name="User").first(), 'qa1', False, "qa"),
        'qa2': ('qa2@example.com', 13124556847, Department.query.filter_by(name=u"测试部").first(),
                Role.query.filter_by(name="User").first(), 'qa2', False, "qa"),
        'dba1': ('dba1@example.com', 13321542635, Department.query.filter_by(name=u"DBA部").first(),
                 Role.query.filter_by(name="User").first(), 'dba1', False, "dba"),
        'dba2': ('dba2@example.com', 13214512245, Department.query.filter_by(name=u"DBA部").first(),
                 Role.query.filter_by(name="User").first(), 'dba2', False, "dba"),
        'user1': ('user1@example.com', 13412115694, Department.query.filter_by(name=u"活动部").first(),
                  Role.query.filter_by(name="User").first(), 'user1', False, "user"),
        'user2': ('user2@example.com', 13451489521, Department.query.filter_by(name=u"行政部").first(),
                  Role.query.filter_by(name="User").first(), 'user2', False, "user"),
        'user3': ('user3@example.com', 13465218952, Department.query.filter_by(name=u"营销中心").first(),
                  Role.query.filter_by(name="User").first(), 'user3', False, "manager"),
        'user4': ('user4@example.com', 13462548991, Department.query.filter_by(name=u"管理中心").first(),
                  Role.query.filter_by(name="User").first(), 'user4', False, "manager"),
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
        user.type = users[u][6]
        db.session.add(user)
    db.session.commit()
    print "Insert user test data."


def idc_insert_data():
    idcs = {
        u'周浦': '',
        u'北京南路': '',
        u'欧阳路': '',
        u'万国数据中心': '',
        u'Ucloud': '',
        u'aliyun': '',
        u'北京酒仙桥': '',
        u'金华双线': '',
        u'宁波三线': '',
        u'无锡线路': '',
        u'南京联通': '',
        u'青岛联通': '',
    }
    for s in idcs:
        idc = Idc.query.filter_by(name=s).first()
        if idc is None:
            idc = Idc(name=s)
        idc.description = idcs[s]
        db.session.add(idc)
    db.session.commit()
    print "Insert idc test data."


def server_insert_data():
    servers = {
        u'zp-prd-app-10': (
            Idc.query.filter_by(name=u"周浦").first(), "K1", '10.10.10.10', '', u'大数据', "PRD", "server",
            u"Online", ""),
        u'zp-prd-app-11': (
            Idc.query.filter_by(name=u"周浦").first(), "K2", '10.10.10.11', '', u'大数据', "PRD", "server",
            u"Online", ""),
        u'oyl-stg-app-101': (
            Idc.query.filter_by(name=u"欧阳路").first(), "R11", '10.18.23.101', '', u'网站部', "STG", "server",
            u"Online", ""),
        u'oyl-stg-app-102': (
            Idc.query.filter_by(name=u"欧阳路").first(), "R11", '10.18.23.102', '', u'网站部', "STG", "server",
            u"Online", ""),
        u'dev-oracle-21': (
            Idc.query.filter_by(name=u"北京南路").first(), "A01", '172.16.11.21', '', u'IT部', "DEV", "vserver",
            u"Online", ""),
        u'dev-oracle-22': (
            Idc.query.filter_by(name=u"北京南路").first(), "A01", '172.16.11.22', '', u'IT据', "DEV", "vserver",
            u"Online", ""),
        u'px-prd-app-10': (
            Idc.query.filter_by(name=u"万国数据中心").first(), "K1", '10.88.10.10', '', u'大数据', "PRD", "server",
            u"Online", ""),
        u'px-prd-app-11': (
            Idc.query.filter_by(name=u"万国数据中心").first(), "K2", '10.88.10.11', '', u'大数据', "PRD", "server",
            u"Online", ""),
        u'uc-stg-app-101': (
            Idc.query.filter_by(name=u"Ucloud").first(), "R11", '10.99.123.101', '', u'网站部', "STG", "server",
            u"Online", ""),
        u'uc-stg-app-102': (
            Idc.query.filter_by(name=u"Ucloud").first(), "R11", '10.99.123.102', '', u'网站部', "STG", "server",
            u"Online", ""),
        u'wx-oracle-21': (
            Idc.query.filter_by(name=u"无锡线路").first(), "A01", '172.16.11.21', '', u'IT部', "DEV", "vserver",
            u"Online", ""),
        u'wx-oracle-22': (
            Idc.query.filter_by(name=u"无锡线路").first(), "A01", '172.16.11.22', '', u'IT据', "DEV", "vserver",
            u"Online", ""),
    }
    for s in servers:
        server = Server.query.filter_by(name=s).first()
        if server is None:
            server = Server(name=s)
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
    print "Insert server test data."


def project_insert_data():
    projects = {
        u'bd-blink': (Department.query.filter_by(name=u"管理中心").first(),
                             User.query.filter_by(username=u'user1').first(), '99999'),
        u'bd-tiger': (Department.query.filter_by(name=u"管理中心").first(),
                             User.query.filter_by(username=u'user2').first(), '99999'),
        u'bd-cmdb': (Department.query.filter_by(name=u"运维部").first(),
                             User.query.filter_by(username=u'ops1').first(), '999'),
        u'bd-bdmp': (Department.query.filter_by(name=u"运维部").first(),
                     User.query.filter_by(username=u'ops2').first(), '999'),
        u'bd-test': (Department.query.filter_by(name=u"开发部").first(),
                     User.query.filter_by(username=u'dev1').first(), '999'),
        u'bd-test2': (Department.query.filter_by(name=u"开发部").first(),
                     User.query.filter_by(username=u'dev2').first(), '999'),
        u'bd-test3': (Department.query.filter_by(name=u"开发部").first(),
                      User.query.filter_by(username=u'dev1').first(), '999'),
        u'bd-jenkins': (Department.query.filter_by(name=u"测试部").first(),
                     User.query.filter_by(username=u'qa1').first(), '999'),
        u'bd-qa': (Department.query.filter_by(name=u"测试部").first(),
                        User.query.filter_by(username=u'qa2').first(), '999'),
        u'bd-oracle': (Department.query.filter_by(name=u"DBA部").first(),
                        User.query.filter_by(username=u'dba1').first(), '999'),
        u'bd-mongodb': (Department.query.filter_by(name=u"DBA部").first(),
                       User.query.filter_by(username=u'dba2').first(), '999'),
    }
    for s in projects:
        project = Project.query.filter_by(name=s).first()
        if project is None:
            project = Project(name=s)
        project.department = projects[s][0]
        project.pm = projects[s][1]
        project.sla = projects[s][2]
        db.session.add(project)
    db.session.commit()
    print "Insert project test data."


def module_insert_data():
    modules = {
        u'bd-blink-server': (Project.query.filter_by(name=u"bd-blink").first(), 'http://10.10.10.5/svn/bd-blink/',
                             User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                             User.query.filter_by(username=u'ops1').first(),
                             Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-tiger-web': (Project.query.filter_by(name=u"bd-tiger").first(), 'http://10.10.10.5/svn/bd-tiger/',
                          User.query.filter_by(username=u'dev2').first(), User.query.filter_by(username=u'qa2').first(),
                          User.query.filter_by(username=u'ops2').first(),
                          Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-cmdb': (Project.query.filter_by(name=u"bd-cmdb").first(), 'http://10.10.10.5/svn/bd-cmdb/',
                     User.query.filter_by(username=u'dev2').first(), User.query.filter_by(username=u'qa2').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-bdmp': (Project.query.filter_by(name=u"bd-bdmp").first(), 'http://10.10.10.5/svn/bd-bdmp/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-test': (Project.query.filter_by(name=u"bd-test").first(), 'http://10.10.10.5/svn/bd-test/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-test2': (Project.query.filter_by(name=u"bd-test2").first(), 'http://10.10.10.5/svn/bd-test2/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-test3': (Project.query.filter_by(name=u"bd-test3").first(), 'http://10.10.10.5/svn/bd-test3/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-jenkins': (Project.query.filter_by(name=u"bd-jenkins").first(), 'http://10.10.10.5/svn/bd-jenkins/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-qa': (Project.query.filter_by(name=u"bd-qa").first(), 'http://10.10.10.5/svn/bd-qa/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-oracle': (Project.query.filter_by(name=u"bd-oracle").first(), 'http://10.10.10.5/svn/bd-oracle/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),

        u'bd-mongodb': (Project.query.filter_by(name=u"bd-mongodb").first(), 'http://10.10.10.5/svn/bd-mongodb/',
                     User.query.filter_by(username=u'dev1').first(), User.query.filter_by(username=u'qa1').first(),
                     User.query.filter_by(username=u'ops2').first(),
                     Software.query.filter_by(version=u'tomcat_7.0.68').first()),
    }
    for m in modules:
        module = Module.query.filter_by(name=m).first()
        if module is None:
            module = Module(name=m)
        module.project = modules[m][0]
        module.svn = modules[m][1]
        module.dev = modules[m][2]
        module.qa = modules[m][3]
        module.ops = modules[m][4]
        module.software = modules[m][5]
        db.session.add(module)
    db.session.commit()
    print "Insert module test data."


def environment_insert_data():
    environments = {
        u'bd-blink-server': (Module.query.filter_by(name=u"bd-blink-server").first(), 'PRD',
                             Idc.query.filter_by(name=u'周浦').first(), "http://www.blink.com/status",
                             "/opt/app/bd-blink-server/", "www.blink.com"),

        u'bd-tiger-web': (Module.query.filter_by(name=u"bd-tiger-web").first(), 'PRD',
                          Idc.query.filter_by(name=u'周浦').first(), "http://www.tiger.com/status",
                          "/opt/app/bd-tiger-web/", "www.tiger.com"),

        u'bd-cmdb': (Module.query.filter_by(name=u"bd-cmdb").first(), 'PRD',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.cmdb.com/status",
                     "/opt/app/bd-cmdb/", "www.cmdb.com"),

        u'bd-bdmp': (Module.query.filter_by(name=u"bd-bdmp").first(), 'PRD',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.bdmp.com/status",
                     "/opt/app/bd-bdmp/", "www.bdmp.com"),

        u'bd-test': (Module.query.filter_by(name=u"bd-test").first(), 'DEV',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.test.com/status",
                     "/opt/app/bd-test/", "www.test.com"),

        u'bd-test2': (Module.query.filter_by(name=u"bd-test2").first(), 'DEV',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.test2.com/status",
                     "/opt/app/bd-test2/", "www.test2.com"),

        u'bd-test3': (Module.query.filter_by(name=u"bd-test3").first(), 'DEV',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.test3.com/status",
                     "/opt/app/bd-test3/", "www.test3.com"),

        u'bd-jenkins': (Module.query.filter_by(name=u"bd-jenkins").first(), 'QA',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.jenkins.com/status",
                     "/opt/app/bd-jenkins/", "www.jenkins.com"),

        u'bd-qa': (Module.query.filter_by(name=u"bd-qa").first(), 'QA',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.qa.com/status",
                     "/opt/app/bd-qa/", "www.qa.com"),

        u'bd-oracle': (Module.query.filter_by(name=u"bd-oracle").first(), 'STG',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.oracle.com/status",
                     "/opt/app/bd-oracle/", "www.oracle.com"),

        u'bd-mongodb': (Module.query.filter_by(name=u"bd-mongodb").first(),  'STG',
                     Idc.query.filter_by(name=u'周浦').first(), "http://www.mongodb.com/status",
                     "/opt/app/bd-mongodb/", "www.mongodb.com"),
    }
    for e in environments:
        environment = Environment(
            module=environments[e][0],
            env=environments[e][1],
            idc=environments[e][2],
            check_point1=environments[e][3],
            deploy_path=environments[e][4],
            domain=environments[e][5])
        db.session.add(environment)
        db.session.commit()
    print "Insert environment test data."
