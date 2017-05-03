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
>>> from app import models
>>> admin = User(username='admin', email='admin@example.com', password='admin', role=Role.query.filter_by(name="Administrator").first(), mobile=13129388374, department="admin", allow_login=True)
>>> db.session.add(admin)
>>> db.session.commit()
```

### user del
```shell
python manage.py shell
>>> from app import models
>>> user = User.query.filter_by(username='user').first()
>>> db.session.delete(user)
>>> db.session.commit()
```

