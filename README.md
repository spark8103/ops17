# ops17

------

## Link
[db-op](/docs/db.md)

[design](/docs/design.md)

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


### api
http://www.bradcypert.com/writing-a-restful-api-in-flask-sqlalchemy/

https://blog.igevin.info/posts/flask-rest-serialize-deserialize/