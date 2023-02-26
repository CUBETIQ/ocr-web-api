#!/bin/sh -e

# python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app
python3 -m flask run --reload