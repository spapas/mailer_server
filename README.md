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
If you want to use my configuration (from /etc)
1. mkdir /home/serafeim/mailer_server/redis/
1. use provided /etc/redis.conf for redis configuration
1. If you want to use supervisord, you can use provided /etc/mailer-server-redis-supervisord.conf

Steps to deploy
---------------

1. Create a database named mailer_server
1. Configure redis - I recommend using a single redis instance for each app
1. Create a parent folder - I used /home/serafeim/mailer_server
1. cd /home/serafeim/mailer_server
1. git clone https://github.com/spapas/mailer_server
1. virtualenv venv
1. mkdir static
1. cd /home/serafeim/mailer_server/mailer_server
1. pip install -r requirements/prod.txt
1. cd /home/serafeim/mailer_server/mailer_server/mailer_server/settings/
1. cp local.py.template local.py
1. Edit local.py and configure your settings
1. echo export DJANGO_SETTINGS_MODULE=mailer_server.settings.prod >> /home/serafeim/mailer_server/venv/bin/activate

Configuring workers
-------------------

You need to run at least one django-rq worker. I recommend using my configuration from
/etc/mailer-server-rqworker-supervisord.conf