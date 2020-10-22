mailer_server
=============

A mailer server for use with your own SMTP server. You install the app, configure it with your SMTP server and can use the API (and other features) to send emails. 

Some features

* A full REST API for sending emails
* Supports attachments to emails
* Supports email templates and distribution list to send emails to many people
* History of sent emails
* Integration with Django through https://github.com/spapas/django-mailer-server-backend

Rationale
---------

One common need of your applications is to send transactional email to their users. If you want to use your own SMTP server (instead of a
mail sending service) you'll soon find out that sending email through SMTP may take some time (even seconds 
depending on your SMTP server) and you'll probably want to make it asynchronous after a little while. The problem is that configuring the
asynchronous infrastracture needed (celery or rq or whatever) just for this kind of job is not worth it. You shouldn't need to install all
these dependencies and moving parts just to be able to send a couple of emails. This project should help you with
this. You install this in a server and then use the API to call it when you send the email. The API is asynchronous and will answer very
fast (some ms) so you the users won't experience any extra delay.

There are various other goodies like seeing the emails that have been sent, allowing for email templates and distribution lists (for
users to create their own lists and send email to these people) and even a django email backend (https://github.com/spapas/django-mailer-server-backend) which you can configure django with so as to use the mailer server for all emails.

You shouldn't use this project if you use something like mailgun or sendgrid or another similar email provider but if you still send
emails through your SMTP server you will find this project invaluable. We're using it in our organization for many years as a 
centralized email sending service and it's used by more than 10 different applications. Also, if you have a *single* app then
you also don't need this; just configure django-rq for this particular app! This project is helpful if you are an organization
that have (or going to have) a handful of different apps that will want to send transactional email.

Requirements
------------

- python 3.x
- virtualenv
- redis
- postgresql (recommended - you can use mysql of sqlite if you know the consequences)
- supervisord (recommended - you can use whatever method you want to run your workers)
- gunicorn (recommended - you can use any wsgi server you want, i.e uwsgi, apache mod_wsgi etc)
- nginx (recommended - you can use any web server you want)

Configuring redis
-----------------
If you want to use my configuration (from etc)

1. ``mkdir /home/serafeim/mailer_server/redis/``
1. use provided ``etc/redis.conf`` for redis configuration
1. If you want to use supervisord, you can use provided ``etc/mailer-server-redis-supervisord.conf``

Steps to deploy
---------------

1. Create a database named mailer_server
1. Create a parent folder for storing app - I used ``/home/serafeim/mailer_server``
1. ``cd /home/serafeim/mailer_server``
1. ``git clone https://github.com/spapas/mailer_server``
1. ``python3 -m venv venv``
1. ``mkdir static``
1. ``cd /home/serafeim/mailer_server/mailer_server``
1. ``pip install -r requirements/prod.txt``
1. ``cp mailer_server/settings/local.py.template mailer_server/settings/local.py``
1. Edit ``local.py`` and configure your settings
1. ``echo export DJANGO_SETTINGS_MODULE=mailer_server.settings.prod >> /home/serafeim/mailer_server/venv/bin/activate``
1. ``source ../venv/bin/activate``
1. ``python manage.py createsuperuser``
1. ``cp /home/serafeim/mailer_server/mailer_server/etc/mlrsrv.ini /home/serafeim/mailer_server/mlrsrv.ini
1. ``sh ./run_gunicorn.sh``

This will run the app through uwsgi as a daemon, listening on unix socket /tmp/mlrsrv.ini (which can be changed directly from
the ``mlrsrv.ini`` uwsgi configuration file). 
Log is at /home/serafeim/mailer_server/uwsgi_mlrsrv.log, pid file at /home/serafeim/mailer_server/mailer_server.pid.

To reload(or stop) use: ``uwsgi --reload(stop) /home/serafeim/mailer_server/mailer_server.pid``

Configuring workers
-------------------

You need to run at least one django-rq worker. I recommend using supervisord with
my configuration from ``etc/mailer-server-rqworker-supervisord.conf``. After the rqworker
is configured please visit http://site_url:8001/admin/django-rq/ - you must
have at least 1 worker there.

Using supervisord
-----------------

Please find the .conf on mailer_server/etc:

1. mailer-server-redis-supervisord.conf for configuring local redis instance (using a unix socket)
1. mailer-server-uwsgi-supervisord.conf for running uwsgi through supervisord
1. mailer-server-rqworker-supervisord.conf for configuring a worker

Running on windows
------------------

I use windows as my development environment and I usually feel like the child of a lesser god when trying to run
stuff on my dev env. However, this project *can* be run on windows (for development only)! Now, as a general tip, I propose the following
directory structure for a django project on windows: Add a ``mailer_server`` parent directory and inside it create
a python virtual environment named ``venv`` and a ``mailer_server`` (cloned from github) that will contain manage.py etc.

- Install redis for windows from here: https://github.com/MSOpenTech/redis/releases and run it - it will listen on default port 6379
- Notice that you can also install redis in a WSL and it will work fine
- Activate the virtual environment: Run dovenv.bat from inside ``mailer_server/mailer_server``
- Install this package https://github.com/michaelbrooks/rq-win/blob/master/rq_win/worker.py using `pip install git+https://github.com/michaelbrooks/rq-win.git#egg=rq-win`
- Run the development server from inside the virtual env through rsp.bat
- Run the windows rq-worker from inside another virtual env through win_rqworker.bat
- You may now visit http://127.0.0.1:8000 and try adding jobs

Authentication and Authorization
-------------------------------

Please configure the project to use the proper authentication method; right now it allows only LDAP (check out `prod.py` for production settings).

To give permissions to your users, you'll need to first create a superuser (using `python manage.py createsuperuser`) and then go to the django-admin and give the `Application admin` or `Application user` perms to your users or groups.
