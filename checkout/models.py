# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from crypton import settings
from django import forms
from django.db import connection
from django.core.cache import get_cache
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from main.msgs import notify_email, pins_reset_email, notify_admin_withdraw_fail
from main.http_common import generate_key_from, start_show_pin, delete_show_pin, generate_key, generate_key_from2, \
    format_numbers10, format_numbers_strong

from sdk.image_utils import ImageText, draw_text, pin
from main.subscribing import subscribe_connection
from datetime import datetime
import math

from Crypto.Cipher import AES
import base64


# Create your models here.
DEBIT_CREDIT = (
    ("in", u"debit"),
    ("out", u"credit"),
)

BOOL = (
    ("true", u"true"),
    ("false", u"false"),
)

STATUS_ORDER = (
    ("manually", u"ручная"),
    ("deposit", u"депозит"),
    ("withdraw", u"вывод"),
    ("bonus", u"партнерское вознаграждение"),
    ("payin", u"пополнение"),
    ("comission", u"коммиссионные"),
    ("created", u"создан"),
    ("incifition_funds", u"недостаточно средств"),
    ("currency_core", u"валюты счетов не совпадают"),
    ("processing", u'в работе'),
    ("processing2", u'в работе 2'),
    ("canceled", u'отменен'),
    ("wait_secure", u'ручная обработка'),
    ("order_cancel", u"отмена заявки"),
    ("deal", u"сделка"),
    ("auto", u"автомат"),
    ("automanually", u"мануальный автомат"),
    ("deal_return", u"возврат маленького остатка"),
    ("processed", u'исполнен'),
    ("core_error", u'ошибка ядра'),
)


def checksum(Obj):
    return True





class TransIn(models.Model):
    ref = models.CharField(max_length=255,
                             verbose_name=u"Наш референс",
                             editable=True,
                             blank=False,
                             null=False)

    title = models.CharField(max_length = 255,
                             verbose_name = u"Title",
                             editable = False,
                             blank = False,
                             null = False )

    description = models.CharField(max_length=255,
                                   verbose_name=u"Description",
                                   blank=True,
                                   null=True)
    currency = models.ForeignKey("Currency",
                                 verbose_name=u"Валюта",
                                 editable=True)

    amnt = models.DecimalField(max_digits=18,
                               decimal_places=2,
                               verbose_name=u"Amount",
                               editable=True)

    user = models.ForeignKey(User, verbose_name=u"Мерчант",
                             related_name="user",
                             editable=True, null=True)


    pub_date = models.DateTimeField(auto_now=False, verbose_name=u"Дата", editable=False)

    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', editable=True)

    order = models.CharField(max_length=255,
                             editable=False,
                             verbose_name=u"order_id"
                             )


    address = models.CharField(max_length=255, blank=True, null=True,
                               editable=False)

    sign = models.CharField(max_length=255, blank=True, null=True,
                            editable=False)


    def fields4sign(self):
        List = []
        for i in ('phone', 'debit_credit', 'status', 'user', 'comission', 'amnt', 'description'):
            Val = getattr(self, i)
            if i in ('comission', 'amnt'):
                List.append(format_numbers_strong(Val))
            else:
                List.append(str(Val))

        return ",".join(List)


    def verify(self, key):
        Fields = self.fields4sign()
        Sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        return Sign == self.sign

    def sign_record(self, key):
        Fields = self.fields4sign()
        self.sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        self.save()


    class Meta:
        verbose_name = u'LiqPay ордер'
        verbose_name_plural = u'LiqPay ордеры'

    ordering = ('id',)

    def __unicode__(o):
        return str(o.id) + " " + str(o.amnt) + " " + o.user.username
