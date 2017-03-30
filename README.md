# ops17

------

## Link
[db-op](/docs/db.md)

[design](/docs/design.md)

## Init
### Install requirements
pip install -r requirements/requirements.txt

### Create db file
python manage.py db upgrade

### init db
```shell
python manage.py shell   

from app import models
Role.insert_roles()
Software.insert_softwares()
User.insert_users()
```

### Run Server
```shell
python manage.py runserver --threaded
```


### api
http://www.bradcypert.com/writing-a-restful-api-in-flask-sqlalchemy/

https://blog.igevin.info/posts/flask-rest-serialize-deserialize/