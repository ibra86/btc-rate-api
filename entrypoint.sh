#!/usr/bin/env bash

exec gunicorn -b 0.0.0.0:5000 --log-level debug wsgi:app
