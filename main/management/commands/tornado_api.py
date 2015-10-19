# -*- coding: utf-8 -*-

__author__ = 'bogdan'
from django.core.management.base import BaseCommand, CommandError

import os
import os.path
import sys
import logging
from crypton.tornado_urls import application_urls
from main.tornado.api import TornadoServer
import crypton.settings


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'start api tornado server'

    def handle(self, *args, **options):
        try:
            debug = args[0]
        except:
            setup_logging()

        worker = TornadoServer.create_instance(8081, application_urls)
        worker.start()


def setup_logging():
    print "setup logging"
    logger = logging.getLogger('main.tornado.api')
    # remove all handlers
    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    filename = "tornado_api.log"
    ch = logging.FileHandler(filename, mode='a')
    logging.Formatter('%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s')
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    

