#!/usr/bin/env python3

__package__ = 'archivebox.cli'
__command__ = 'archivebox celery'

import subprocess
import sys


def main(*args, **kwargs) -> None:
    print('Starting Celery..')
    subprocess.call('/app/celery_run.sh')


if __name__ == '__main__':
    main(args=sys.argv[1:], stdin=sys.stdin)
