# -*- coding: utf-8 -*-

# Create your views here.
from django.template import Context, loader
from django.http import  HttpResponse 
from crypton import settings
from django.utils.translation import ugettext as _
from django.utils import formats

from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import UserCustomSettings, VolatileConsts, OrdersMem, Accounts, TradePairs, Orders, Trans, Currency, Msg, add_trans, TransError, StockStat, OnlineUsers
from django.views.decorators.cache import cache_page
from main.http_common import caching, cached_json_object, my_cache, status_false, json_auth_required, auth_required, check_api_sign
from main.http_common import format_numbers10, format_numbers_strong, format_numbers, format_numbers4, json_false500, json_true
import logging
logger = logging.getLogger(__name__)
from main.models import dictfetchall, to_prec, OrderTimer, add_trans2
from  main.msgs  import system_notify
import json
import decimal
from decimal import Decimal, getcontext
import datetime
import calendar
import time
from datetime import timedelta
from main.my_cache_key import my_lock, my_release, LockBusyException, check_freq

from tornaduv import UVLoop
import tornado.web
import tornaduv
import pyuv


@json_auth_required
def sell(Req, Trade_pair):   
                FreqKey = "orders" + str(Req.user.id)
                Start = time.time()
                if not check_freq(FreqKey, 3):
                    Response =   HttpResponse('{"status":false,"description":false}')
                    Response['Content-Type'] = 'application/json'
                    return Response
                
                getcontext().prec = settings.TRANS_PREC
                
                try :
                        Count = Req.REQUEST.get("count")
                        Price = Req.REQUEST.get("price")
                        Count  = Decimal( Count.replace(",",".").strip() )
                        Price  = Decimal( Price.replace(",",".").strip() ) 
                        Count = to_prec(Count, settings.TRANS_PREC )                      
                        Price = to_prec(Price, settings.TRANS_PREC )                      
                        
                except:
                        Response =   HttpResponse(process_mistake(Req, "invalid_params"))
                        Response['Content-Type'] = 'application/json'
                        return Response
                
                if Price <= 0:
                        Response =   HttpResponse(process_mistake(Req, "SumLess0"))
                        Response['Content-Type'] = 'application/json'
                        return Response
                        
                if Count<=0:
                        Response =   HttpResponse(process_mistake(Req, "CountLess0"))
                        Response['Content-Type'] = 'application/json'
                        return Response
                
                TradePair =  TradePairs.objects.get(url_title = Trade_pair) 
                LOCK = "trades" + TradePair.url_title
                
                if TradePair.min_trade_base > Count:
                        Response =   HttpResponse(process_mistake(Req, "MinCount"))
                        Response['Content-Type'] = 'application/json'
                        
                        return Response
                        
                Custom = "0.0005" #Req.session["deal_comission"] 
                Comission = Decimal(Custom)
                
                CurrencyOnS = Req.REQUEST.get("currency") 
                CurrencyBaseS  = Req.REQUEST.get("currency1")
                Amnt1 = Count
                Amnt2 = Count * Price
                
                CurrencyBase = Currency.objects.get(title =  CurrencyBaseS )
                CurrencyOn = Currency.objects.get(title =  CurrencyOnS )
                TradeLock = my_lock(LOCK)
                order = Orders( user = Req.user,
                                currency1 = CurrencyOn,
                                currency2 = CurrencyBase, 
                                sum1_history = Amnt1,
                                sum2_history = Amnt2,
                                price = Price,
                                sum1 = Amnt1, 
                                sum2 = Amnt2,
                                transit_1 = TradePair.transit_on,
                                transit_2 = TradePair.transit_from,
                                trade_pair = TradePair,
                                comission = Comission
                                )
                
                order.save()

                try: 
                        FromAccount = Accounts.objects.get(user = Req.user, currency = CurrencyOn)
                        add_trans(FromAccount, Amnt1, CurrencyOn, TradePair.transit_on, order, "deposit")                      
                        order.status = "processing"
                        order.sign_record(str(Req.user.id))
                        order.save()
                        system_notify(deposit_funds(order), Req.user.id)
                        MemOrder = order.mem_order(str(Req.user.id) )
                        ResAuto = make_auto_trade(MemOrder, TradePair, MemOrder.price, CurrencyOn, Amnt1, CurrencyBase, Amnt2)
                        if MemOrder.status == "processed":
                            MemOrder.make2processed()
                        else:
                            MemOrder.sign_record(str(Req.user.id))

                        my_release(TradeLock)
                        Response = HttpResponse(process_auto(Req, ResAuto, TradePair))
                        Response['Content-Type'] = 'application/json'
                        
                        End = time.time()
                        measure = OrderTimer(order = order,time_work = str(End - Start))
                        measure.save()
                        
                        return Response 
                except TransError as e: 
                        order.status = "canceled"
                        order.save()
                        Status = e.value
                        my_release(TradeLock)
                        Response =   HttpResponse(process_mistake(Req, Status))
                        Response['Content-Type'] = 'application/json'
                        End = time.time()
                        measure = OrderTimer(order = order,time_work = str(End - Start))
                        measure.save()
                        return Response