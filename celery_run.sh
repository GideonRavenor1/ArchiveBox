#!/bin/bash

set -e

cd /app/archivebox/ && celery worker -A core.celery -c 4 -l warning
