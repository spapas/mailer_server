mailer_server
=============

Requirements
------------

- python 2.7
- virtualenv
- redis
- postgresql (recommeneded - you can use mysql of sqlite if you know the consequences)
- supervisord (recommended - you can use whatever method you want to run your workers)
- uwsgi (recommended - you can use any wsgi server you want, i.e gunicorn, apache mod_wsgi etc)
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
1. ``virtualenv venv``
1. ``mkdir static``
1. ``cd /home/serafeim/mailer_server/mailer_server``
1. ``pip install -r requirements/prod.txt``
1. ``cp mailer_server/settings/local.py.template mailer_server/settings/local.py``
1. Edit ``local.py`` and configure your settings
1. ``echo export DJANGO_SETTINGS_MODULE=mailer_server.settings.prod >> /home/serafeim/mailer_server/venv/bin/activate``
1. ``source ../venv/bin/activate``
1. ``python manage.py createsuperuser``
1. ``sh ./run_uwsgi.sh``

This will run the app through uwsgi as a daemon, listening on port 8001. 
Log is at /home/serafeim/mailer_server/uwsg.log, pid file at /home/serafeim/mailer_server/mailer_server.pid.

To reload(or stop) use: ``uwsgi --reload(stop) /home/serafeim/mailer_server/mailer_server.pid``

Configuring workers
-------------------

You need to run at least one django-rq worker. I recommend using supervisord with
my configuration from ``etc/mailer-server-rqworker-supervisord.conf``. After the rqworker
is configured please visit http://site_url:8001/admin/django-rq/ - you must
have at least 1 worker there.