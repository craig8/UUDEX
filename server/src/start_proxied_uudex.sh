#!/bin/bash

# proxied server
# starts gunicorn on localhost http port 8080, expect nginx to handle all ssl.  nginx passes client cert info in http header

export APP_ENV=GunicornProxied
nohup gunicorn --log-level debug --config gunicorn_proxied.conf.py gunicorn_start 2> server_err.out 1> server.out &
