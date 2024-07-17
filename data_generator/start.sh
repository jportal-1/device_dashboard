#!/usr/bin/env bash

service rabbitmq-server start
celery -A tasks worker -B --loglevel=INFO -c 2