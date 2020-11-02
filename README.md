# mailer_server


A mailer server for use with your own SMTP server. You install the app, configure it with your SMTP server and can use the API (and other features) to send emails. 

## Some features

* A full REST API for sending and searching sent emails
* Supports attachments to emails
* Supports email templates and distribution list to send emails to many people
* History of sent emails
* Integration with Django through https://github.com/spapas/django-mailer-server-backend

## Rationale

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

## Requirements

- python 3.x
- virtualenv
- redis
- postgresql (recommended - you can use mysql of sqlite if you know the consequences)
- supervisord (recommended - you can use whatever method you want to run your workers)
- gunicorn (recommended - you can use any wsgi server you want, i.e uwsgi, apache mod_wsgi etc)
- nginx (recommended - you can use any web server you want)

## Configuring redis

If you want to use my configuration (from etc)

1. ``mkdir /home/serafeim/mailer_server/redis/``
1. use provided ``etc/redis.conf`` for redis configuration
1. If you want to use supervisord, you can use provided ``etc/mailer-server-redis-supervisord.conf``

## Steps to deploy


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

## Configuring workers


You need to run at least one django-rq worker. I recommend using supervisord with
my configuration from ``etc/mailer-server-rqworker-supervisord.conf``. After the rqworker
is configured please visit http://site_url:8001/admin/django-rq/ - you must
have at least 1 worker there.

## Using supervisord

Please find the .conf on mailer_server/etc:

1. mailer-server-redis-supervisord.conf for configuring local redis instance (using a unix socket)
1. mailer-server-uwsgi-supervisord.conf for running uwsgi through supervisord
1. mailer-server-rqworker-supervisord.conf for configuring a worker

Please consider that I no longer recommend using supervisord. Nowadays I recommend configuring systemd jobs for your services. Here's an example for the `mailer_server.service` (gunicorn app server). Create a file named `/etc/systemd/system/mlrsrv.service` with the following contents:

```
[Unit]
Description=mailer_server.hcg.gr app server

[Service]
Type=simple
User=serafeim
ExecStart=/home/serafeim/mailer_server/venv/bin/gunicorn --workers=4 --bind=unix:/home/serafeim/mailer_server/gunicorn.sock --chdir=/home/serafeim/mailer_server/mailer_server/ mailer_server.wsgi
WorkingDirectory=/home/serafeim/mailer_server/
Restart=always
KillMode=process
RestartSec=5
After=network.target

Environment=DJANGO_SETTINGS_MODULE=mailer_server.settings.prod
Environment=HTTPS_PROXY=http://proxy.com:8080
Environment=HTTP_PROXY=http://proxy.com:8080
Environment=https_proxy=http://proxy.com:8080
Environment=https_proxy=http://proxy.com:8080

[Install]
WantedBy=multi-user.target
```

Then run `systemctl daemon-reload` to read the new unit, `systemctl start mailer_server` to start the service and `systemctl enable mailer_server` to make it run at boot. You should add similar units for the workers and the redis backend.

## Running on windows

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

Using the API
-------------

Send single email

```
curl -v -H "Content-Type: application/json" -H "Authorization: Token CHANGE_WITH_YOUR_TOKEN"      -X POST --data @apicall.txt http://MAILER.SERVER.ADDRESS/mail/api/send_mail/
```

where, apicall.txt contains the mail data in JSON:

```
{
    "subject": "Email subject",
    "body": "body body foo bar baz taz",
    "mail_from": "from@from.gr",
    "mail_to": "to@from.gr",
    "reply_to": "reply@repl.gr",
    "cc": "cc@cc.gr",
    "bcc": "bcc@cc.gr",
    "body_type": "plain"
}
```

## Send mass email



```curl -v -H "Content-Type: application/json" -H "Authorization: Token CHANGE_WITH_YOUR_TOKEN"  -X POST --data @massapicall.txt http://MAILER.SERVER.ADDRESS/mail/api/send_mass_mail/```

where, massapicall.txt contains the mass mail data in JSON:

```
{
    "mail_template": 1,
    "distribution_list_to": 1
}
```

Send email with attachment

You'll need to post multipart/form-data for this to work. Here's how 

```curl -v -H "Content-Type: multipart/form-data" -H "Authorization: Token CHANGE_WITH_YOUR_TOKEN"  -X POST -F subject=world -F body="hello world" -F attachment=@apicall.txt -F attachment=@massapicall.txt  http://MAILER.SERVER.ADDRESS/mail/api/send_mass_mail/```


Usage
-----
     
An email address can take two forms. Either
        
* name@email.com, or 
* ull name &lt;name@email.com&gt;
        
These two forms can be used anywhere (i.e in the mail_from address, mail_to list of addresses etc) but 
please don't use comma (',') to the Full name of the recipient because it is used as a separator between
email addresses.

Templates and distribution lists
--------------------------------

The users of this app can create template emails that also contain attachments than you can then send to distribution lists.
The distribution lists can either edited by hand or you can import/export CSV files with the name/email pairs of the recipients.
