from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import Partnership, Currency, add_trans, Accounts

from decimal import getcontext
import sys
from main.my_cache_key import my_lock, my_release, LockBusyException

PARTNERSHIP = 2259
# user_ref = models.ForeignKey( User, verbose_name = u"Клиент", related_name = "partner" )
#user = models.ForeignKey( User, verbose_name = u"Приведенный клиент", related_name = "join_by_parnter" )
#url_from = models.CharField(verbose_name=u"URL from", max_length = 255,default="direct")
#income = models.CharField(verbose_name=u"доход", max_length = 255,default="0")
#income_from = models.DateTimeField( verbose_name = u"Дата пересчета", editable = False )
#status =  models.CharField( max_length = 40,
#choices = STATUS_ORDER,
#default = 'created', editable = False)
#class Meta:
#verbose_name=u'Референс'
#verbose_name_plural = u'Референсы'
# TODO TEST IT
# it's not working
class Command(BaseCommand):
    args = '<Stock Title ...>'
    help = 'every minute get stock prices and save it to StockStat'

    def handle(self, *args, **options):
        ##hardcode UAH income
        CurIns = Currency.objects.get(id=1)
        AccountFrom = Accounts.objects.get(user=PARTNERSHIP,
                                           currency=CurIns)
        for icome in Partnership.objects.filter(status="processing"):
            AccountTo = Accounts.objects.get(user=AccountFrom.income.user,
                                             currency=CurIns)
            AccountFrom.income.status = "processed"
            income.save()
            add_trans(AccountFrom, income.income, CurIns, AccountTo, None, "payin", str(income.id), False)
            