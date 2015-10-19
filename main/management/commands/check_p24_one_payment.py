from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in, cancel_p24_in, TradePairs, P24TransIn
import crypton.settings


def get_p24():
    from sdk.p24 import p24

    return p24("UAH", "https://api.privatbank.ua/", crypton.settings.P24_MERCHID, crypton.settings.P24_PASSWD)


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    # def add_arguments(self, parser):
    #       parser.add_argument('args')

    def handle(self, *args, **options):
        from sdk.p24 import p24
        # for item in P24TransIn.objects.filter(status='processing'):
        #	TradePair = TradePairs.objects.get(url_title = "p24")
        for i in [113720]:
            D = get_p24()

            item = Orders.objects.get(id=i)
            Res = D.check_payment(item.id, True)

            if item.status == "processing":
                #item.order.status='processing'
                #item.save()
                if Res == 1:
                    process_p24_in(item.id, D.description, D.comis)
                    item.status = 'processed'

                if Res == 0:
                    cancel_p24_in(item.id)
                    item.status = 'canceled'
                        
                    
                    
       
