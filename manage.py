#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import multiprocessing
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")
sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'magpie.settings'

from modules.template.depend.listen import dnslog, jndi

try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antenna.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
        # p = multiprocessing.Process(target=dnslog.main)
        # p2 = multiprocessing.Process(target=jndi.main)
        # p.daemon = True
        # p2.daemon = True
        # p.start()
        # p2.start()
        pass
    execute_from_command_line(sys.argv)
