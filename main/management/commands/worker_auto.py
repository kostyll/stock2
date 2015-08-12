from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from main.models import CardP2PTransfers, ObjectionsP2P,get_decrypted_user_pin,p2p_inner_process,get_comisP2P
import time
from datetime import timedelta
from django.contrib.auth.models import User
import os
import sys
from main.my_cache_key import my_lock, my_release, LockBusyException
from crypton import settings
from main.models import FullBinInfo

def get_p24():
        from sdk.p24 import p24
        return p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD,settings.P24MERCH_CARD)



class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
    
        LOCK = "p2p_lock_auto"
        lock = my_lock(LOCK)            
        try :
            process_command()
            my_release(lock)                        
        except :
                print "Unexpected error:", sys.exc_info()[0]    

        


def process_command():
        Now = datetime.now()
        l1 = list(CardP2PTransfers.objects.filter(status = "processing"))
        l2 = list(CardP2PTransfers.objects.filter(status = "processing2"))
        for item in l1+l2:
                print "process  %s to card %s date %s amnt is %s" %   (item.user.username,
                                                                        item.CardNumber,
                                                                        item.pub_date,
                                                                        item.amnt )
                P24 = get_p24()
                Card = item.CardNumber
                Card.replace(" ","")
                Bin = Card[:6]
                if 1 and  not item.verify(get_decrypted_user_pin(item.user)):
                    print "SALT FAILED"
                    continue
                else:
                    print "Salt ok"
                
                try :
                    Objection = ObjectionsP2P.objects.get(CardNumber = Card)
                    pay2p(item, P24)

                    print "its not new card %s" % (Card) 
                    continue
                    
                except ObjectionsP2P.DoesNotExist:
                        print "its new card %s" % (Card) 
                        
                try:
                        IsPb =  FullBinInfo.objects.get(bin6 = Bin, pbbin = "1")
                        Objection = ObjectionsP2P(CardNumber = Card, Objection = "2")
                        Objection.save()
                        pay2p(item, P24)                            


                except FullBinInfo.DoesNotExist:
                    print "i didn't find %s" % (Card)
                    continue 
                        
def pay2p(item, P24):
    admin_system = User.objects.get(id = 1)
    item.status = "processed"
    item.save()
    Result = None
    CardNumber = item.CardNumber
    CardNumber.replace(" ","")
    try :
           NewAmnt = get_comisP2P(CardNumber, item.amnt )
           Result = P24.pay2p(item.id, CardNumber, NewAmnt)
    except TransError as e:
           item.status = "core_error"
           item.save()
    except Exception as e:
           i.status = "core_error"
           i.save()

    if Result :
         p2p_inner_process(admin_system, item)
    else:
         item.status = "core_error"
         item.save()
 
