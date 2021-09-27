# My Blog

##

### Setup

```sh
$ mkdir /blog/api
$ python --version
$ python -m venv venv-blog
$ source venv-blog/bin/activate
$ pip install --upgrade pip
$ pip install django==3.1.7
$ django-admin startproject blog_api
$ cd blog_api/
$ mv blog_api/ config
$ mkdir apps/users
$ mkdir apps/core
$ python manage.py startapp users apps/users/
$ python manage.py startapp users apps/users
$ python manage.py startapp core apps/core
$ pip freeze
$ pip freeze > requirements.txt
$ less requirements.txt
  asgiref==3.4.1
  Django==3.1.7
  pytz==2021.1
  sqlparse==0.4.2
  typing-extensions==3.10.0.2
```

## Git setup
