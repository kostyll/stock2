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
	Date = args[0]
	Cancel  = False
	if len(args) > 1:
		Cancel = int(args[1])
	
	Date = datetime.strptime(Date,"%Y-%m-%d")
        remove_orders(Date, Cancel)
       


def remove_orders( Date , Cancel ):
	processed_orders={}
	man2process = {}
        for item in Trans.objects.filter(pub_date__gte=Date).filter(Q(status='deposit')|Q(status="deal")|Q(status="comission")|Q(status='order_cancel')):
	    if  item.user2_id  in (1972, 9) or item.user1_id  in (9,28,13,14,15,3910,4367,7816, 33305, 363):
		continue
	    
	   # print("%i " %item.id)
	   # print "%i,%i" % ( item.order_id, int(item.out_order_id))
	    if item.status == "deal" or item.status == "order_cancel":
		ItemDeposit = Trans.objects.get(status="deposit", order_id=item.order_id)
		if ItemDeposit.pub_date >= Date:
			for item2cancel  in Trans.objects.filter(order_id = item.order_id):
			    if not processed_orders.has_key(item2cancel.id):
				cancel_trans(item2cancel, Cancel)
				processed_orders[item2cancel.id]=1
	        else:
		    if  search_trans_before(item.order_id,  Date):
			if not man2process.has_key(item.order_id):
		        	man2process[item.order_id] = [item, ItemDeposit]
			else:
				man2process[item.order_id].append(item)			
		
	       	
		ItemDeposit = Trans.objects.get(status="deposit", order_id=item.out_order_id)
		if ItemDeposit.pub_date >= Date:
			for item2cancel  in Trans.objects.filter(order_id = item.order_id):
			    if not processed_orders.has_key(item2cancel.id):
				cancel_trans(item2cancel, Cancel)
				processed_orders[item2cancel.id]=1
			
		else:
		    if  search_trans_before(item.out_order_id,  Date):
			if not man2process.has_key(int(item.out_order_id)):
		        	man2process[int(item.out_order_id)] = [item, ItemDeposit]
			else:
				man2process[int(item.out_order_id)].append(item)			
        process_transes = {}
	for trans_list in  man2process.keys():
	    print "process order %i" % trans_list
	    List = search_trans_before(trans_list, Date)
	    for item in man2process[trans_list] + List:
		if not  process_transes.has_key(item.id):
			print "%i %i to %i %s %s %s %s" % (item.id,item.user1_id,item.user2_id,item.pub_date,item.status, item.amnt, str(item.currency) )
			process_transes[item.id] = True

	    

def search_trans_before(order_id, Date):
	List = list(Trans.objects.filter(pub_date__lt=Date, status='deal').filter(Q(out_order_id=str(order_id))|Q(order_id=order_id)))
	for item in List:
	#	print("%s %s %s" % (item.status, str(item.pub_date), item.id))
		return List
	return False


def cancel_trans(obj, Cancel):	
    if Cancel:	
	add_trans(obj.user2, 
		  obj.amnt,
		  obj.currency, 
		  obj.user1, 
		  None, 
		  "canceled", 
		  obj.id, 
		  False)                 
