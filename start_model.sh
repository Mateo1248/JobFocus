#!/bin/bash

nohup gunicorn -p /tmp/model.pid --workers 2 --timeout 10000 --keep-alive 1000 --bind 127.0.0.1:8003 wsgi_model:app 0<&- &> /var/log/model.log &

echo "model started!"
