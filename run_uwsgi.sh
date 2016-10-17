uwsgi --http-socket=0.0.0.0:8001 --module=mailer_server.wsgi:application --processes=2 --pidfile=/home/serafeim/mailer_server/mailer_server.pid -d /home/serafeim/mailer_server/uwsgi.log
