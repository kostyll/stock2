from django.core.management.base import BaseCommand, CommandError
from main.models import  Orders, TradePairs, Trans,add_trans
from django.db import connection
from datetime import datetime
from decimal import getcontext
import sys
from django.db.models import Q

class Command(BaseCommand):
  args = '<Stock Title ...>'
  help = 'every minute get stock prices and save it to StockStat'

  def handle(self, *args, **options):
        Date = args[1]
        Date = datetime.strptime(Date,"%Y-%m-%d")
        Account = int(args[0])
        checking(Account, Date)

def checking(Account, Date, Eps=0.1):
        prev = None
        signs = {}
        for item in Trans.objects.filter(pub_date__gte=Date).filter(Q(user2_id=Account)|Q(user1_id=Account)).order_by("id"):
            print "%i %s"% (item.id, item.fields4sign())
            if prev is None:
                if Account == item.user2_id:
                        prev = {"balance": item.res_balance2}
                else:
                        prev = {"balance": item.res_balance1}
                continue

            item.sign_record()
            sign = item.sign
            if signs.has_key(item.sign):
                print item.sign
                signs[sign] = True
                print "check double operation"
                sys.exit(0)

            if item.res_balance2 is None and item.status=='incifition_funds':
                continue

            if Account == item.user2_id:

              if abs(item.balance2 - prev["balance"])<Eps :
                  prev = {"balance": item.res_balance2 }
              else:
                  print "check2 wait %s got %s" % (prev["balance"], item.balance2)
                  sys.exit(0)
            else:

              if abs(item.balance1 - prev["balance"])<Eps :
                  prev = {"balance": item.res_balance1 }
              else:
                  print "check2 wait %s got %s" % (prev["balance"], item.balance1)
                  sys.exit(0)

            if item.verify():
                print "normal"
            else:
                temp_sign = item.sign
                item.sign_record()
                got_sign = item.sign
                print " wait %s got %s" % (temp_sign, got_sign)
                sys.exit(0)
