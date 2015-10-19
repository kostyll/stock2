# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import UserCustomSettings
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext as _
import crypton.settings
import urllib2
import time
import json
import sys
from main.subscribing import subscribe_connection
from django.core import mail

from django.template import Context, loader


class Command(BaseCommand):
    args = ''
    help = 'reset pins for all users'

    def handle(self, *args, **options):
        BaseUrl = crypton.settings.BASE_URL
        ##using it's own api
        Decoder = json.JSONDecoder()
        Url = BaseUrl + "api/trades/sell/btc_uah?_=%s" % (str(time.localtime()))
        Str = None
        try:
            D = urllib2.urlopen(Url)
            Str = D.read()
        except:
            sys.exit(0)

        Url = BaseUrl + "api/trades/buy/btc_uah?_=%s" % (str(time.localtime()))
        StrBuy = None
        try:
            D = urllib2.urlopen(Url)
            StrBuy = D.read()
        except:
            sys.exit(0)

        ResBuy = Decoder.decode(StrBuy)
        Res = Decoder.decode(Str)
        # ResList =  []
        #for item in Res["list"]:
        Dict = {"orders": Res["list"],
                "whole_sum": Res["orders_sum"],
                "whole_sum_buy": ResBuy["orders_sum"],
                "buy_orders": ResBuy["list"]
        }

        tmpl = loader.get_template("rates_subscribe.html")
        c = Context(
            Dict
        )
        Connection = subscribe_connection()

        text_content = tmpl.render(c)
        for item in UserCustomSettings.objects.filter(setting__title="rate_notify"):
            if item.value == "yes" and item.user.email != '':
                print "send message to %s email %s " % (item.user.username, item.user.email)
                msg = EmailMultiAlternatives(_(u"Уведомление о курсах BTC TRADE UA"),
                                             text_content, crypton.settings.SERVER_EMAIL,
                                             [item.user.email], connection=Connection)
                msg.attach_alternative(text_content, "text/html")
                try:
                    msg.send()
                except:
                    print "Unexpected error:", sys.exc_info()[0]

                time.sleep(1)
