#!/bin/env python
# coding: utf-8

import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from app import create_app, db
from app.models import User, Role, Software, Permission
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Software=Software, Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


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
    from app.models import Role, Software, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create software
    Software.insert_softwares()

    # create test User
    admin = User(username='admin', email='admin@example.com', password='admin',
                 role=Role.query.filter_by(name="Administrator").first(),
                 mobile=13129388374, department="admin", allow_login=True)
    ops = User(username='ops', email='ops@example.com', password='ops',
               role=Role.query.filter_by(name="User").first(),
               mobile=13854263519, department="ops")
    dev = User(username='dev', email='dev@example.com', password='dev',
               role=Role.query.filter_by(name="User").first(),
               mobile=13625486549, department="dev")
    qa = User(username='qa', email='qa@example.com', password='qa',
              role=Role.query.filter_by(name="User").first(),
              mobile=13752461259, department="qa")
    user = User(username='user', email='user@example.com', password='user',
                role=Role.query.filter_by(name="User").first(),
                mobile=13245682136, department="user")
    db.session.add(admin)
    db.session.add(ops)
    db.session.add(dev)
    db.session.add(qa)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    deploy()
