from __future__ import with_statement
from fabric.api import *
import os

def pep8():
    "Do pep8 styule checks"
    print "Check with pep8"
    # local('pep8 --max-line-length=160 --filename=*.py mailer_server --exclude migrations')
    print "pep8 ok!"

def commit():
    local('git add .')
    with settings(warn_only=True):
        local('git commit')
    with settings(warn_only=True):
        local('git push origin master')
    print "Commit ok"

def pull():
    with cd(env.directory):
        run('git fetch origin')
        run('git merge origin/master')
    print "fetch / merge ok"

def work():
    "Do work on server (copy settings, migrate and run collect static)"
    with cd(env.directory):
        requirements_txt = 'requirements/'+env.env+".txt"
        if os.stat(requirements_txt).st_size > 0:
            virtualenv('pip install -r {0}'.format(requirements_txt) )
        virtualenv('python manage.py migrate')
        virtualenv('python manage.py update_permissions')
        virtualenv('python manage.py collectstatic --noinput')
        virtualenv('python manage.py compress')

def touch_wsgi():
    print("Restarting uwsgi");
    run("supervisorctl restart mailerserveruwsgi")
    print("Restarting rqworker");
    run("supervisorctl restart mailerserverrqworker")

def full_deploy():
    "Commit - pull - do work - and restart uwsgi"
    pep8()
    commit()
    pull()
    work()
    touch_wsgi()

def virtualenv(command):
    run(env.activate + '&&' + command)


def uat():
    "UAT settings"
    env.env = "uat"
    env.user = 'serafeim'
    env.hosts = ['uat1.hcg.gr']
    env.directory = '/home/serafeim/mailer_server/mailer_server'
    env.activate = 'source /home/serafeim/mailer_server/venv/bin/activate'

def prod():
    "PROD settings"
    env.env = "prod"
    env.user = 'serafeim'
    env.hosts = ['devapps.hcg.gr']
    env.directory = '/home/serafeim/mailer_server/mailer_server'
    env.activate = 'source /home/serafeim/mailer_server/venv/bin/activate'

