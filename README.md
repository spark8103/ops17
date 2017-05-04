# ops17
ops17是运维管理平台，以flask+mysql为框架开发的。
------

## Link
[design](/docs/design.md)

[db-op](/docs/db.md)

[api-op](/docs/api.md)

## Init
### Install requirements
pip install -r requirements/requirements.txt
python manage.py db init

### Migrate db
python manage.py db migrate

### Create db file
python manage.py db upgrade

### init db
python manage.py init_db

```shell
python manage.py shell   

from app import models
Role.insert_roles()
Software.insert_softwares()
```

### Run Server
```shell
python manage.py runserver --threaded
```