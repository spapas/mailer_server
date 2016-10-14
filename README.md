mailer_server
=============

Deploying
---------

Requirements

- python 2.7
- virtualenv


1. Create a parent folder - I used /home/serafeim/mailer_server
2. cd /home/serafeim/mailer_server
3. git clone https://github.com/spapas/mailer_server
4. virtualenv venv
5. mkdir static
6. cd /home/serafeim/mailer_server/mailer_server
7. pip install -r requirements/prod.txt
8. cd /home/serafeim/mailer_server/mailer_server/mailer_server/settings/
9. cp local.py.template local.py
10. Edit local.py
11. echo export DJANGO_SETTINGS_MODULE=dgul.settings.prod >> /home/serafeim/mailer_server/venv/bin/activate

