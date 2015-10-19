from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in, cancel_p24_in, TradePairs
import crypton.settings
from decimal import Decimal
from main.msgs import notify_email
from main.models import add_trans, LiqPayTrans


class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    # def add_arguments(self, parser):
    #       parser.add_argument('args')

    def handle(self, *args, **options):
        from sdk.liqpay import liqpay

        for DebCred in LiqPayTrans.objects.filter(status='processing', debit_credit='in'):
            order = DebCred.order
            OrderId = order.id
            d = liqpay("ru", "UAH")
            Dict = d.api("payment/status", {"version": "2", "order_id": str(OrderId)})
            print Dict
            if Dict["status"] == "success":
                if order.status != "processing":
                    DebCred.status = 'canceled'
                    DebCred.save()
                    continue
                order.status = "processing2"
                order.save()
                OutOrderId = Dict["liqpay_order_id"]
                from main.models import check_holds

                check_holds(order)
                add_trans(order.transit_1, order.sum1, d.currency,
                          order.transit_2, order,
                          "payin", OutOrderId, False)

                #hack if privat is wrong
                Comission = Decimal(Dict["receiver_commission"])
                Phone = Dict['sender_phone']
                Desc = Dict['description']
                Signature = Dict['liqpay_order_id']
                Amount = Dict['amount']
                add_trans(order.transit_2, Comission, d.currency,
                          order.transit_1, order,
                          "comission", OutOrderId, False)

                DebCred.status = 'processed'
                DebCred.save()
                order.status = "processed"
                order.save()
                #notify_email(order.user, "deposit_notify", DebCred )
        else:
            DebCred.status = 'canceled'
            DebCred.save()
		
                    
       
