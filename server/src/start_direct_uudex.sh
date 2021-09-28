#!/bin/bash

# unproxied server
# starts gunicorn so it's directly facing client and gunicron handles all ssl

export APP_ENV=Gunicorn
nohup gunicorn --log-level debug --config gunicorn_direct.conf.py gunicorn_start 2> server_err.out 1> server.out &
