# My Blog

## Main

### API Setup

```s
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

### Git setup

```s
$ git init
Initialized empty Git repository in /Users/douzez/Development/blog/api/blog_api/.git/
$ vi .gitignore
  esc --> i --> start typing
  esc  --> :wq!
$ git status
$ git add .
$ git commit -m "configure blog api project"
$ git branch -M main
$ git branch
$ git remote add origin https://github.com/douzez/blog-api.git
$ git remote remove origin
$ git remote add origin git@github.com:douzez/blog-api.git
$ git push -u origin main
$ git checkout -b users
```
