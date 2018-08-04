#!/bin/sh

pipenv run gunicorn --config /app/gunicorn.conf.py --log-level info -b :8080 main:app
