## Course Django 2021 ##

**Source repo**
https://github.com/divanov11/Django-2021

**Install virtualenv**
pip install virtualenv

**Create venv**
python -m virtualenv venv01

**Activate env**
venv01\Scripts\activate

**Install packages**
pip install -r requirements.txt

**Run**
python manage.py runserver

**admin**
python manage.py createsuperuser

**Create app**
python manage.py startapp users

**Migrations**
python manage.py makemigrations
python manage.py migrate

**Shell**
python manage.py shell

**static files for prod (debug false)**
python manage.py collectstatic

**Steps to add form**
Create template
Create View
Create URL
Add new url in navbar or as a link
Create Form (define fields to show + style)
Add Form to View
To add more style to form, copy from form-template.html
