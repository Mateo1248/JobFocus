#!/bin/bash

nohup gunicorn -p /tmp/app1.pid --workers 1 --timeout 240 --keep-alive 120 --bind 127.0.0.1:8001 wsgi_app:app 0<&- &> /var/log/app1.log &
nohup gunicorn -p /tmp/app2.pid --workers 1 --timeout 240 --keep-alive 120 --bind 127.0.0.1:8002 wsgi_app:app 0<&- &> /var/log/app2.log &

echo "app started!"
