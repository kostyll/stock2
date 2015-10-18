#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    parent_dir = os.path.abspath(os.path.dirname(__file__)) # get parent_dir path
    sys.path.append(parent_dir)
    sys.path.append("/home/btctrade/stock/local/lib/python2.7/site-packages")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypton.settings")

    from django.core.management import execute_from_command_line
    reload(sys)
    sys.setdefaultencoding('utf-8')

    execute_from_command_line(sys.argv)
