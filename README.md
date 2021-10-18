# My Blog

## Main

### API models architecture

- URLs

  Authentication (POST, PATCH, DELETE)

  - /api/users
  - /api/users/:id
  - /api/blog/tags (post)
  - /api/blog/tags/:tag_slug (patch - change name)

  No Authentication (GET)

  - /api/blog/posts ==> DONE
  - /api/blog/posts?page=3 ==> DONE with pagination
  - /api/blog/posts/:slug ==> In PROGRESS
  - /api/blog/tags (get) ==> DONE
  - /api/blog/tags/:tag_slug (get) ==> DONE with posts(slug)

- Models

- Users - get_user_model

  - email, password, password2?
  - token

- Posts

  - id
  - title
  - slug
  - body
  - description
  - publish
  - image
  - thumbnail
  - created_at
  - updated_at
  - tags - ManyToMany to Tags

- Tags

  - id
  - name
  - slug
  - ManyToMany to Posts

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
$ python manage.py startapp users
$ python manage.py startapp core
$ pip freeze
$ pip freeze > requirements.txt
$ less requirements.txt
  asgiref==3.4.1
  Django==3.1.7
  pytz==2021.1
  sqlparse==0.4.2
  typing-extensions==3.10.0.2
$ python manage.py startapp blog
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

### REST Setup

$ pip install django-rest-framework==0.1.0
$ pip install django-cors-headers==3.7.0
