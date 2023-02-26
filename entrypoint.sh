#!/bin/sh -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-5000}

python3 -m gunicorn --bind ${HOST}:${PORT} wsgi:app