# -*- coding: utf-8 -*-

__author__ = 'bogdan'
from django.core.management.base import BaseCommand, CommandError

import os
import os.path
import sys
import logging
from crypton.tornado_urls import application_urls
from main.tornado.api import TornadoServer


class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'start api tornado server'

    def handle(self, *args, **options):
          worker = TornadoServer.create_instance(8081, application_urls)
    

          worker.start()

