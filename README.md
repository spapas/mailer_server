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

This will run the app through uwsgi as a daemon, listening on port 8001 (which can be changed directly from
the ``run_uwsgi.sh`` script). 
Log is at /home/serafeim/mailer_server/uwsg.log, pid file at /home/serafeim/mailer_server/mailer_server.pid.

To reload(or stop) use: ``uwsgi --reload(stop) /home/serafeim/mailer_server/mailer_server.pid``

Configuring workers
-------------------

You need to run at least one django-rq worker. I recommend using supervisord with
my configuration from ``etc/mailer-server-rqworker-supervisord.conf``. After the rqworker
is configured please visit http://site_url:8001/admin/django-rq/ - you must
have at least 1 worker there.

Running on windows
------------------

I use windows as my development environment and I usually feel like the child of a lesser god when trying to run
stuff on my dev env. However this project *can* be run on windows! Now, as a general tip, I propose the following
directory structure for a django project on windows: Add a ``mailer_server`` parent directory and inside it create
a python virtual environment named ``venv`` and a ``mailer_server`` (cloned from github) that will contain manage.py etc.

- Install redis for windows from here: https://github.com/MSOpenTech/redis/releases and run it - it will listen on default port 6379
- Activate the virtual environment: Run dovenv.bat from inside ``mailer_server/mailer_server``
- Run the development server from inside the virtual env through rsp.bat
- Run the windows rq-worker from inside another virtual env through win_rqworker.bat
- You may now visit http://127.0.0.1:8000