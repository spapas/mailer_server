uwsgi --http-socket=0.0.0.0:8001 --module=mailer_server.wsgi:application --processes=2 --master
