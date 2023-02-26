#!/bin/sh -e

docker build . -t registry1.ctdn.net/library/ocr-web-api:latest

docker push registry1.ctdn.net/library/ocr-web-api:latest
