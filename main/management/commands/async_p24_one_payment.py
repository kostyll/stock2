from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in2, cancel_p24_in, TradePairs, P24TransIn
import crypton.settings
def get_p24():
        from sdk.p24 import p24
        return p24("UAH", "https://api.privatbank.ua/", crypton.settings.P24_MERCHID, crypton.settings.P24_PASSWD)


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
#    def add_arguments(self, parser):
 #       parser.add_argument('args')

    def handle(self, *args, **options):
        from sdk.p24 import p24
        for item in P24TransIn.objects.filter(status='processing'):
            TradePair = TradePairs.objects.get(url_title = "p24")
            D = get_p24() 
            Res = D.check_payment(item.order_id, True)

            if  item.status == "processing":
                item.status='processing2'
                print item.user.username
                print item.amnt
                item.save()
                if Res == 1 :
                    print "status normal"
                    process_p24_in2(item.order.id, D.description, D.comis, item )    
                    item.status='processed'
                        
                if Res == 0:
                    cancel_p24_in(item.id)
                    item.status='canceled'    
                            
                item.save()                    
                    
       
