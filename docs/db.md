# db op

------

## DB op and update

#### create migrations repo

```shell
python manage.py db init
```

#### migrations db

```shell
python manage.py db migrate -m "initial migration"
```

#### update db
```shell
python manage.py db upgrade
```

#### downgrade db
```shell
python manage.py db downgrade
```

#### create_all db
```shell
python manage.py db create_all
```

## role init
```shell
python manage.py shell
>>> from app import models
>>> Role.insert_roles()
>>> Role.query.all()
```

### user add
```shell
python manage.py shell
```

```shell
from app import models
Role.insert_roles()
admin = User(username='admin', email='admin@example.com', password='admin', role=Role.query.filter_by(name="Administrator").first(), mobile=13129388374, department="admin", allow_login=True)
ops = User(username='ops', email='ops@example.com', password='ops', role=Role.query.filter_by(name="User").first(), mobile=13854263519, department="ops")
dev = User(username='dev', email='dev@example.com', password='dev', role=Role.query.filter_by(name="User").first(), mobile=13625486549, department="dev")
qa = User(username='qa', email='qa@example.com', password='qa', role=Role.query.filter_by(name="User").first(), mobile=13752461259, department="qa")
user = User(username='user', email='user@example.com', password='user', role=Role.query.filter_by(name="User").first(), mobile=13245682136, department="user")
db.session.add(admin)
db.session.add(ops)
db.session.add(dev)
db.session.add(qa)
db.session.add(user)
db.session.commit()
```