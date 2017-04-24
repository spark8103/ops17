#!/usr/bin/env python
# coding: utf-8
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import User, Role, Department, Idc, Server, Permission, Software, Project, Module, Environment
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# logger file setting
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('logs/ops.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('bd-cmdb logging startup')

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Department=Department, Idc=Idc, Server=Server,
                Permission=Permission, Software=Software, Project=Project, Module=Module, Environment=Environment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()


@manager.command
def init_db():
    """Init db and insert test data."""
    from flask_migrate import init, migrate, upgrade
    if prompt_bool(
            'Are you sure you want to init your data'):
        # migrate database to latest revision
        upgrade()
        Role.insert_roles()
        Department.insert_departments()
        Department.insert_departments()
        Software.insert_softwares()
        Idc.insert_idcs()
        User.insert_users()
        Server.insert_servers()


@manager.command
def drop_db():
    """Drop all db tables"""
    if prompt_bool(
            'Are you sure you want to lose all your data'):
        db.drop_all()
        result = db.engine.execute("DROP TABLE IF EXISTS `ops`.`alembic_version`")
        print "delete version table: " + str(result)


if __name__ == '__main__':
    manager.run()
