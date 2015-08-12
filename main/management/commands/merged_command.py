from django.core.management.base import BaseCommand, CommandError
from main.models import  Orders, TradePairs
from main.api import  return_rest2acc, order_finish
from  main.msgs  import system_notify
from django.db import connection
from datetime import datetime
from decimal import getcontext
import sys
from django.core.management import call_command

from main.my_cache_key import my_lock, my_release, LockBusyException


class Command(BaseCommand):
  args = '<Stock Title ...>'
  help = 'every minute get stock prices and save it to StockStat'

  def handle(self, *args, **options):
        LOCK = "merged_command_"
        
        try:
               lock = my_lock(LOCK)
#		*  *  *   *   *     cd crypton;python ./manage_lock.py clean_small_orders btc_uah >> clean_small.log
#*  *  *   *   *     cd crypton;python ./manage_lock.py clean_small_orders ltc_uah >> clean_small.log
#*  *  *   *   *     cd crypton;python ./manage_lock.py clean_small_orders nvc_uah >> clean_small.log
#*/1  *  *   *   *   cd crypton;python ./manage_lock.py clear_online >> clear_online.log
#*/2  *  *   *   *     cd crypton;python ./manage_lock.py stock_stat  1>>stock_stat.log 2>>stock_stat.log
#*/3   *  *   *   *     cd crypton;python ./manage.py top_prices >> top_prices.log
	       call_command('uah_balance')
	       call_command('liqapy_async')
	       call_command('async_p24_one_payment')

	       call_command('clear_online')
	       call_command('top_prices')
	       call_command('stock_stat')
	       call_command('clean_small_orders', 'btc_uah')
	       call_command('clean_small_orders', 'ltc_uah')
	       call_command('clean_small_orders', 'nvc_uah')
	       call_command('clean_small_orders', 'doge_uah')
	       call_command('rates_uah_usd')	
	
        except LockBusyException as e:
               print "operation is locked", e.value
        except:
               print "Unexpected error:", str(sys.exc_info())
        finally:
	        my_release(lock)
       
                 
                 
