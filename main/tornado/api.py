# -*- coding: utf-8 -*-

import json
from decimal import Decimal, getcontext
import datetime
import calendar
import time


# from tornaduv import UVLoop
import tornado.web
# import tornaduv
# import pyuv
import threading
# Create your views here.

from django.template import Context, loader

from crypton.http import HttpResponse
from crypton import settings
from django.utils.translation import ugettext as _
from django.utils import formats

from django.db import connection
from django.contrib.auth.models import User
from main.models import UserCustomSettings, VolatileConsts, OrdersMem, Accounts, TradePairs, Orders, Trans, Currency, \
    Msg, add_trans, TransError, StockStat, OnlineUsers

from main.api_http_common import caching, cached_json_object, my_cache, status_false, json_auth_required, check_api_sign
from main.api_http_common import format_numbers10, format_numbers_strong, format_numbers, format_numbers4, \
    json_false500, json_true

import logging

logger = logging.getLogger(__name__)
from main.models import dictfetchall, to_prec, OrderTimer, add_trans2, DealsMemory
from  main.msgs import system_notify

from datetime import timedelta
from main.my_cache_key import my_lock, LockBusyException, check_freq, my_release

from crypton.http import MemStore

import timeit
from threadpool import ThreadPool, WorkRequest


class TornadoServer(object):
    # статический экземпляр этого класса, всегда один
    # доступ к нему только через TornadoServer.get_instance()
    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Возвращает экземпляр ядра, если оно создано.
        :rtype : Core
        """
        if not cls._instance:
            raise RuntimeError('core is not created')
        return cls._instance

    @classmethod
    def is_created(cls):
        """
        Создано ли ядро?
        :rtype : bool
        """
        return cls._instance is not None

    @classmethod
    def create_instance(cls, *args):
        """
        Создаёт и возвращает объект ядра с настройками из объекта settings или из файла по settings_path.
        :rtype : Core
        """
        logging.debug('creating tornado instance')
        cls._instance = TornadoServer(*args)
        logging.debug('core created: {0}'.format(cls._instance))
        return cls._instance


    def __init__(self, *args):
        self.port = args[0]
        self.application = tornado.web.Application(args[1])
        # self.core_event_loop = pyuv.Loop.default_loop()
        self.memstore = MemStore.create_instance()
        # tornado.ioloop.IOLoop.configure(UVLoop)
        # tornado.ioloop.IOLoop.current().initialize(self.core_event_loop)

    # start eventloop, webserver and periodic reading
    def start(self):
        self.application.listen(self.port)
        self.main_loop = tornado.ioloop.IOLoop.instance()
        self.main_loop.start()


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug("stoping tornado")
        tornado.ioloop.IOLoop.instance().stop()


def cache_control(Req):
    do = Req.REQUEST.get("do", None)
    Cache = caching()
    Dict = Cache.get_storage()
    if do == "flush":
        Dict = {}
        Cache.set_storage(Dict)
        return json_true(Req)

    if do == "get":
        key = Req.REQUEST.get("key")
        return HttpResponse(str(Dict[key]))

    if do == "del":
        key = Req.REQUEST.get("key")
        value = str(Dict[key])
        Cache.delete(key)
        return HttpResponse(value)

    return HttpResponse(str(Dict))


def my_async(func2decorate):
    def wrapper(*args, **kwards):
        callable_object = lambda: func2decorate(*args, **kwards)
        main_object = TornadoServer.get_instance()
        request = WorkRequest(callable_object)
        main_object.pool.putRequest(request)

        return True

    return wrapper


def get_account(user, currency):
    return Accounts.objects.get(user_id=user, currency_id=currency)


def deposit_funds(Order, currency1):
    return _("Deposit funds  %(sum)s %(currency)s according with order #%(order_id)i " % {
        'sum': Order.sum1_history,
        'currency': currency1.title,
        'order_id': Order.id})


def order_finish(Order):
    return _("You order #%(order_id)i is fully completed" % {'order_id': Order.id})


def order_return_unused(Order, Currency1, AccumSumToSell):
    return _("Return %(sum).8f %(currency)s unused funds according with order #%(order_id)i  " %
             {'sum': AccumSumToSell,
              'currency': str(Currency1),
              'order_id': Order.id})


def order_description_buy(Sum1, Sum2, Order, BackOrder, TradePair):
    Price = BackOrder.price

    if Order.currency2 == TradePair.currency_on.id:
        return _("Buying %(sum).8f %(currency)s according with order  #%(order_id)i, price %(price).8f  " %
                 {'sum': Sum2,
                  'currency': str(TradePair.currency_on),
                  'order_id': Order.id,
                  'price': Price})
    else:
        return _("Selling  %(sum).8f %(currency)s according with order #%(order_id)i, price %(price).8f  "
                 % {'sum': Sum1,
                    'currency': str(TradePair.currency_on),
                    'order_id': Order.id,
                    'price': Price})


def order_description_sell(Sum1, Sum2, Order, TradePair):
    Price = Order.price
    if Order.currency2 == TradePair.currency_on.id:
        return _("Buying %(sum).8f %(currency)s according with order  #%(order_id)i, price %(price).8f  " % {
            'sum': Sum2,
            'currency': str(TradePair.currency_on),
            'order_id': Order.id,
            'price': Price})
    else:

        return _("Selling  %(sum).8f %(currency)s according with order #%(order_id)i, price %(price).8f  " %
                 {'sum': Sum1,
                  'currency': str(TradePair.currency_on),
                  'order_id': Order.id,
                  'price': Price})


# process order  item that match order Order
def process_order(AccountBuyer, ComisBuy, AccumSum, AccumSumToSell, item, Order, TradePair, ComisSell):
    ## TODO move to settings for every user
    ComisPercentSeller = item.comission
    ComisPercentBuyer = Order.comission
    logging.debug("=========================================================================================")

    logging.debug(item)
    logging.debug("%s%s" % (AccumSum, AccumSumToSell))
    logging.debug(Order)
    logging.debug("=========================================================================================")

    if not item.verify(str(item.user)):
        logging.debug("Sign FAILED %s" % str(item))
        return AccumSum, AccumSumToSell

    if item.sum1 > AccumSum:
        ## a danger of low overflow
        ## TODO remove deviding
        Diff = AccumSum / item.sum1
        # UAH -> BTC * 5600
        # BTC-> UAH / 5600
        # AcumSum => 5600
        # item.sum => 5200
        TransSum = item.sum2 * Diff  # =>AccumSum*item.price
        # TransSum = AccumSumToSell
        AccountSeller = get_account(item.user, item.currency2)
        ##comission
        item.sum1 = item.sum1 - AccumSum
        item.sum2 = item.sum2 - TransSum
        item.sign_record(str(item.user))
        item.save()
        Order.sum2 = 0
        Order.sum1 = AccumSumToSell - TransSum
        Order.save()

        add_trans2(item.transit_2,
                   TransSum,
                   item.currency2,
                   AccountSeller.id,
                   item.id,
                   "deal",
                   Out_order_id=Order.id
        )

        add_trans2(AccountSeller.id,
                   TransSum * ComisPercentSeller,
                   item.currency2,
                   ComisSell.id,
                   item.id,
                   "comission",
                   Out_order_id=Order.id
        )

        add_trans2(item.transit_1,
                   AccumSum,
                   item.currency1,
                   AccountBuyer.id,
                   item.id,
                   "deal",
                   Out_order_id=Order.id
        )

        add_trans2(AccountBuyer.id,
                   AccumSum * ComisPercentBuyer,
                   item.currency1,
                   ComisBuy.id,
                   Order.id,
                   "comission",
                   Out_order_id=Order.id)

        try:
            system_notify_async(order_description_sell(AccumSum, TransSum, item, TradePair), AccountSeller.user.id)
            system_notify_async(order_description_buy(TransSum, AccumSum, Order, item, TradePair), AccountBuyer.user.id)
        except:
            logging.info("something gooing wrong with notification")
            pass

        return 0, Order.sum1

    if item.sum1 <= AccumSum:
        TransSum = item.sum2
        NotifySum = item.sum1
        AccountSeller = get_account(item.user, item.currency2)
        ##comission
        # TODO move to archive
        item.status = "processed"
        item.sum1 = 0
        item.sum2 = 0
        item.save()
        Order.sum2 = AccumSum - NotifySum
        Order.sum1 = AccumSumToSell - TransSum
        Order.save()

        add_trans2(item.transit_2,
                   TransSum,
                   item.currency2,
                   AccountSeller.id,
                   item.id,
                   "deal",
                   Out_order_id=Order.id)

        add_trans2(AccountSeller.id,
                   TransSum * ComisPercentSeller,
                   item.currency2,
                   ComisSell.id,
                   item.id,
                   "comission",
                   Out_order_id=Order.id)

        add_trans2(item.transit_1,
                   NotifySum,
                   item.currency1,
                   AccountBuyer.id,
                   item.id,
                   "deal",
                   Out_order_id=Order.id)

        add_trans2(AccountBuyer.id,
                   NotifySum * ComisPercentBuyer,
                   item.currency1,
                   ComisBuy.id,
                   Order.id,
                   "comission",
                   Out_order_id=Order.id)

        try:
            system_notify_async(order_description_sell(NotifySum, TransSum, item, TradePair), AccountSeller.user.id)
            system_notify_async(order_description_buy(TransSum, NotifySum, Order, item, TradePair),
                                AccountBuyer.user.id)
            system_notify_async(order_finish(item), AccountSeller.user.id)

        except:
            logging.info("somthing gooing wrong with notification")
            pass
        item.make2processed()
        return Order.sum2, Order.sum1


def auth(Req):
    Nonce = Req.REQUEST.get("nonce", None)
    if Nonce is None:
        return json_false500(Req)

    Sign = Req.META.get('HTTP_API_SIGN', None)

    if Sign is None:
        return json_false500(Req, {"description": "invalid_params", "key": "api_sign"})

    PublicKey = Req.META.get('HTTP_PUBLIC_KEY', None)
    if PublicKey is None:
        return json_false500(Req, {"description": "invalid_params", "key": "public_key"})

    try:
        Req.user = check_api_sign(PublicKey, Sign, Req.body)
        Cache = caching()
        Cache.set("nonce_" + PublicKey, int(Nonce), 50000)
        Nonce = Cache.get("nonce_" + PublicKey)
        return json_true(Req, {"nonce": Nonce, "public_key": PublicKey})
    except:
        return json_false500(Req, {"description": "auth_faild"})


def make_auto_trade(Order, TradePair, Price, Currency1, Sum1, Currency2, Sum2):
    ##if we sell
    # Query = "SELECT * FROM main_ordersmem  WHERE  trade_pair_id=%i" % (TradePair.id)

    if int(TradePair.currency_on.id) == int(Currency1.id):
        Query = "SELECT * FROM main_ordersmem  WHERE  currency1=%i AND currency2=%i \
                           AND status='processing' AND price >= %s  \
                           AND user!=%i  ORDER BY price DESC, id DESC" % (Currency2.id,
                                                                          Currency1.id,
                                                                          format_numbers_strong(Price), Order.user)
    else:
        Query = "SELECT * FROM main_ordersmem WHERE  currency1=%i AND currency2=%i \
                           AND status='processing' AND price <= %s \
                           AND user!=%i  ORDER BY price, id DESC " % (Currency2.id,
                                                                      Currency1.id,
                                                                      format_numbers_strong(Price), Order.user )

    List = OrdersMem.objects.raw(Query)

    ##work on first case
    CommissionSell = Accounts.objects.get(user_id=settings.COMISSION_USER, currency=Currency1)
    ComnissionBuy = Accounts.objects.get(user_id=settings.COMISSION_USER, currency=Currency2)
    AccumSumToSell = Sum1
    AccumSum2Buy = Sum2
    AccountBuyer = get_account(Order.user, Currency2.id)
    UserDeals = [int(Order.user)]

    for item in List:
        (AccumSum2Buy, AccumSumToSell) = process_order(AccountBuyer, ComnissionBuy, AccumSum2Buy,
                                                       AccumSumToSell, item, Order,
                                                       TradePair, CommissionSell)
        UserDeals.append(int(item.user))
        if AccumSum2Buy > 0.00000001:
            continue
        else:
            break

    ResultSum = finish_create_order(TradePair, AccumSum2Buy, AccumSumToSell, Order)
    Order.sum1 = AccumSumToSell

    if ResultSum > 0.00000001:
        Order.sum2 = ResultSum
    else:
        Order.sum2 = 0
        Order.status = "processed"


    # if order has rest of funds return all to account
    if AccumSumToSell > 0 and Order.sum2 == 0 and Order.status == "processed":
        return_rest2acc(Order, AccumSumToSell)
        Order.sum1 = 0

    Order.save()

    return {"start_sum": Sum2, "last_sum": ResultSum, "users_bothered": UserDeals}


@my_async
def return_rest2acc(Order, AccumSumToSell):
    Account2Sell = get_account(Order.user, Order.currency1)
    add_trans2(Order.transit_1,
               AccumSumToSell,
               Order.currency1,
               Account2Sell.id,
               Order.id,
               "deal_return")
    system_notify(order_return_unused(Order, Account2Sell.currency, AccumSumToSell), Order.user)


@my_async
def system_notify_async(Msg, User):
    system_notify(Msg, User)


def finish_create_order(TradePair, SumToBuy, AccumSumToSell, Order):
    ##base currency
    if Order.currency1 == TradePair.currency_on:

        if AccumSumToSell < TradePair.min_trade_base:
            system_notify_async(order_finish(Order), Order.user)
            return 0
        else:
            return SumToBuy
    else:
        if SumToBuy < TradePair.min_trade_base:
            system_notify_async(order_finish(Order), Order.user)
            return 0
        else:
            return SumToBuy


@my_async
def reload_cache(Res, Type):
    cache = caching()
    DeleteKeys = []
    for i in Res["users_bothered"]:
        CachedKey1 = 'client_orders_' + str(i) + "_" + Type
        CachedKey2 = 'balance_' + str(i)
        DeleteKeys.append(CachedKey1)
        DeleteKeys.append(CachedKey2)
        # deal_list_btc_uah
    DeleteKeys.append("deal_list_" + Type)
    DeleteKeys.append("sell_list_" + Type)
    DeleteKeys.append("buy_list_" + Type)
    logging.debug("delete this keys %s " % str(DeleteKeys))

    cache.delete_many(DeleteKeys)


def process_auto(Res, TradePair):
    Dict = None
    Encoder = json.JSONEncoder()
    if Res["start_sum"] == Res["last_sum"]:
        Dict = {"status": True, "description": _("The order has been created")}


    elif Res["last_sum"] < TradePair.min_trade_base:
        Dict = {"status": "processed",
                "description": _("Your order has been fully processed successfully"),
                "start_sum_to_buy": str(Res["start_sum"]),
                "last_sum_to_buy": str(Res["last_sum"])
        }
    elif Res["start_sum"] > Res["last_sum"]:
        Dict = {"status": "processed", "description": _("Your order has been  processed partial"),
                "start_sum_to_buy": str(Res["start_sum"]),
                "last_sum_to_buy": str(Res["last_sum"])
        }

    Type = TradePair.url_title
    reload_cache(Res, Type)
    return Encoder.encode(Dict)


def process_mistake(Req, Mistake):
    Dict = None
    Encoder = json.JSONEncoder()

    if Mistake == 'incifition_funds':
        Dict = {"status": Mistake, "description": u"У вас недостаточно средст для этой операции,"
                                                  u" пополните ваш счет во вкладке "
                                                  u"<a href='/finance'> \"финансы\" </a> "}
    elif Mistake == "MinCount":
        Dict = {"status": Mistake, "description": _("Count of deal is too small")}
    elif Mistake == "invalid_params":
        Dict = {"status": Mistake, "description": _("Invalid params")}
    else:
        Dict = {"status": Mistake, "description": _("Some mistake has been occured, "
                                                    "try later, or call support")}
    return Encoder.encode(Dict)


@my_cache
def market_prices(Req):
    Dict = None
    Encoder = json.JSONEncoder()
    prices = []
    for item in TradePairs.objects.filter(status="processing").order_by("ordering"):
        TopName = item.url_title + "_top_price"
        Price = VolatileConsts.objects.get(Name=TopName)
        prices.append({"type": TopName, "price": Price.Value})
    RespJ = Encoder.encode({"prices": prices})
    return RespJ


@json_auth_required
def remove_order(Req, Order):
    Encoder = json.JSONEncoder()

    FreqKey = "orders" + str(Req.user.id)
    if not check_freq(FreqKey, 3):
        Response = HttpResponse('{"status":false}')
        Response['Content-Type'] = 'application/json'
        return Response

    if __inner_remove_order(Order, Req.user):
        Dict = {"status": True}
        RespJ = Encoder.encode(Dict)
        Response = HttpResponse(RespJ)
        Response['Content-Type'] = 'application/json'
        return Response
    else:
        Dict = {"status": False, "description": _("A mistake has been occured during removing try one more")}
        RespJ = Encoder.encode(Dict)
        Response = HttpResponse(RespJ)
        Response['Content-Type'] = 'application/json'
        return Response


def __inner_remove_order(Order, User):
    Order2Remove = OrdersMem.objects.get(user=User.id, id=int(Order), status="processing")
    if not Order2Remove.verify(str(User.id)) and False:
        return False

    Market = TradePairs.objects.get(id=Order2Remove.trade_pair)

    Order2Remove.status = "canceled"
    Order2Remove.save()
    Title = Market.url_title

    LOCK = "trades" + Title
    TradeLock = my_lock(LOCK)

    try:
        Account = Accounts.objects.get(user=User, currency_id=Order2Remove.currency1)
        add_trans2(Order2Remove.transit_1,
                   Order2Remove.sum1,
                   Order2Remove.currency1,
                   Account.id,
                   Order2Remove.id,
                   "order_cancel")

        cache = caching()
        cache.delete_many(["buy_list_" + Title,
                           "sell_list_" + Title,
                           "balance_" + str(User.id),
                           'client_orders_' + str(User.id) + "_" + Title])

        my_release(TradeLock)
        return True
    except:

        my_release(TradeLock)
        return False


@json_auth_required
def sell(Req, Trade_pair):
    FreqKey = "orders" + str(Req.user.id)
    Start = time.time()
    if not check_freq(FreqKey, 3):
        Response = HttpResponse('{"status":false,"description":false}')
        Response['Content-Type'] = 'application/json'
        return Response

    getcontext().prec = settings.TRANS_PREC

    try:
        Count = Req.REQUEST.get("count")
        Price = Req.REQUEST.get("price")
        Count = Decimal(Count.replace(",", ".").strip())
        Price = Decimal(Price.replace(",", ".").strip())
        Count = to_prec(Count, settings.TRANS_PREC)
        Price = to_prec(Price, settings.TRANS_PREC)

    except:
        Response = HttpResponse(process_mistake(Req, "invalid_params"))
        Response['Content-Type'] = 'application/json'
        return Response

    if Price <= 0:
        Response = HttpResponse(process_mistake(Req, "SumLess0"))
        Response['Content-Type'] = 'application/json'
        return Response

    if Count <= 0:
        Response = HttpResponse(process_mistake(Req, "CountLess0"))
        Response['Content-Type'] = 'application/json'
        return Response

    TradePair = TradePairs.objects.get(url_title=Trade_pair)
    LOCK = "trades" + TradePair.url_title

    if TradePair.min_trade_base > Count:
        Response = HttpResponse(process_mistake(Req, "MinCount"))
        Response['Content-Type'] = 'application/json'

        return Response

    Custom = "0.0005"  # Req.session["deal_comission"]
    Comission = Decimal(Custom)

    CurrencyOnS = Req.REQUEST.get("currency")
    CurrencyBaseS = Req.REQUEST.get("currency1")
    Amnt1 = Count
    Amnt2 = Count * Price

    CurrencyBase = Currency.objects.get(title=CurrencyBaseS)
    CurrencyOn = Currency.objects.get(title=CurrencyOnS)
    TradeLock = my_lock(LOCK)
    order = OrdersMem(user=Req.user.id,
                      currency1=CurrencyOn.id,
                      currency2=CurrencyBase.id,
                      sum1_history=Amnt1,
                      sum2_history=Amnt2,
                      price=Price,
                      sum1=Amnt1,
                      sum2=Amnt2,
                      transit_1=TradePair.transit_on.id,
                      transit_2=TradePair.transit_from.id,
                      trade_pair=TradePair.id,
                      comission=Comission,
                      status="processing"
    )

    order.save()
    i = order.id
    try:
        FromAccount = Accounts.objects.get(user=Req.user, currency=CurrencyOn)
        system_notify_async(deposit_funds(order, CurrencyOn), Req.user.id)
        add_trans2(FromAccount.id, Amnt1, CurrencyOn.id, TradePair.transit_on.id, order.id, "deposit")
        order.sign_record(str(Req.user.id))
        ResAuto = make_auto_trade(order, TradePair, order.price, CurrencyOn, Amnt1, CurrencyBase, Amnt2)

        if order.status == "processed":
            order.make2processed()
        else:
            order.sign_record(str(Req.user.id))
        # adding locks
        my_release(TradeLock)
        Response = HttpResponse(process_auto(ResAuto, TradePair))
        Response['Content-Type'] = 'application/json'

        End = time.time()
        measure = OrderTimer(order=i, time_work=str(End - Start))
        measure.save()
        return Response
    except TransError as e:
        order.status = "canceled"
        order.sign_record(str(Req.user.id))
        order.save()
        Status = e.value
        my_release(TradeLock)
        Response = HttpResponse(process_mistake(Req, Status))
        Response['Content-Type'] = 'application/json'
        End = time.time()
        measure = OrderTimer(order=i, time_work=str(End - Start))
        measure.save()
        return Response


@json_auth_required
def buy(Req, Trade_pair):
    FreqKey = "orders" + str(Req.user.id)
    Start = time.time()
    if not check_freq(FreqKey, 3):
        Response = HttpResponse('{"status":false}')
        Response['Content-Type'] = 'application/json'
        return Response

    getcontext().prec = settings.TRANS_PREC
    try:
        Count = Req.REQUEST.get("count")
        Price = Req.REQUEST.get("price")
        Count = Decimal(Count.replace(",", ".").strip())
        Price = Decimal(Price.replace(",", ".").strip())
        Count = to_prec(Count, settings.TRANS_PREC)
        Price = to_prec(Price, settings.TRANS_PREC)

    except:
        Response = HttpResponse(process_mistake(Req, "invalid_params"))
        Response['Content-Type'] = 'application/json'
        return Response

    if Price <= 0:
        Response = HttpResponse(process_mistake(Req, "SumLess0"))
        Response['Content-Type'] = 'application/json'
        return Response

    if Count <= 0:
        Response = HttpResponse(process_mistake(Req, "CountLess0"))
        Response['Content-Type'] = 'application/json'
        return Response

    TradePair = TradePairs.objects.get(url_title=Trade_pair)
    LOCK = "trades" + TradePair.url_title

    if TradePair.min_trade_base > Count:
        Response = HttpResponse(process_mistake(Req, "MinCount"))
        Response['Content-Type'] = 'application/json'
        return Response

    Custom = "0.0005"  # Req.session["deal_comission"]
    Comission = Decimal(Custom)

    CurrencyOnS = Req.REQUEST.get("currency")
    CurrencyBaseS = Req.REQUEST.get("currency1")

    Amnt1 = Price * Count
    Amnt2 = Count

    CurrencyBase = Currency.objects.get(title=CurrencyBaseS)
    CurrencyOn = Currency.objects.get(title=CurrencyOnS)

    TradeLock = my_lock(LOCK)
    order = OrdersMem(user=Req.user.id,
                      currency1=CurrencyBase.id,
                      currency2=CurrencyOn.id,
                      price=Price,
                      sum1_history=Amnt1,
                      sum2_history=Amnt2,
                      sum1=Amnt1,
                      sum2=Amnt2,
                      transit_1=TradePair.transit_from.id,
                      transit_2=TradePair.transit_on.id,
                      trade_pair=TradePair.id,
                      comission=Comission,
                      status="processing"
    )
    order.save()
    i = order.id
    try:
        FromAccount = Accounts.objects.get(user=Req.user, currency=CurrencyBase)
        # order.status = "processing"
        order.save()
        system_notify_async(deposit_funds(order, CurrencyBase), Req.user.id)
        # TODO Order to Encrypted object
        add_trans2(FromAccount.id, Amnt1, CurrencyBase.id, TradePair.transit_from.id, order.id, "deposit")
        order.sign_record(str(Req.user.id))

        ResAuto = make_auto_trade(order, TradePair, order.price, CurrencyBase, Amnt1, CurrencyOn, Amnt2)

        if order.status == "processed":
            order.make2processed()
        else:
            order.sign_record(str(Req.user.id))
        Response = HttpResponse(process_auto(ResAuto, TradePair))
        my_release(TradeLock)
        Response['Content-Type'] = 'application/json'
        End = time.time()
        measure = OrderTimer(order=i, time_work=str(End - Start))
        measure.save()

        return Response
    except TransError as e:


        order.status = "canceled"
        order.sign_record(str(Req.user.id))
        order.save()
        Status = e.value
        Response = HttpResponse(process_mistake(Req, Status))
        Response['Content-Type'] = 'application/json'
        my_release(TradeLock)
        End = time.time()
        measure = OrderTimer(order=i, time_work=str(End - Start))
        measure.save()
        return Response


@json_auth_required
def bid(Req, UrlTitle):
    CurrentTradePair = TradePairs.objects.get(url_title=UrlTitle)
    SumList = []
    Amount = Decimal("0")
    TempSum = Decimal('0')
    try:
        Amount = Decimal(Req.REQUEST.get("amount", None))
        Query = "SELECT * FROM main_ordersmem  WHERE  currency2=%i AND currency1=%i \
                          AND status='processing'  \
                          AND user!=%i  ORDER BY price DESC" % (
            CurrentTradePair.currency_on.id,
            CurrentTradePair.currency_from.id,
            Req.user.id)
        List = OrdersMem.objects.raw(Query)
        for item in List:
            if Amount > item.sum1:
                Amount -= item.sum1
                TempSum += item.sum1
                SumList.append({"sum": item.sum1, "price": item.price})
            else:
                TempSum += Amount
                SumList.append({"sum": Amount, "price": item.price})
                break
    except:
        Response = HttpResponse('{"status":false, "description":"amount is incorrect"}')
        Response['Content-Type'] = 'application/json'
        return Response
        # format_numbers_strong(balance_buy.balance )

    AvaragePrice = Decimal("0")
    BuySum = Decimal("0")
    for item in SumList:
        BuySum += item['sum']
        AvaragePrice += ((item['sum'] / TempSum) * item['price'] )
    Dict = {"sell_sum": format_numbers_strong(BuySum),
            "price": format_numbers_strong(AvaragePrice),
            "status": True}
    RespJ = json.JSONEncoder().encode(Dict)
    return cached_json_object(RespJ)


@json_auth_required
def ask(Req, UrlTitle):
    CurrentTradePair = TradePairs.objects.get(url_title=UrlTitle)
    SumList = []
    Amount = Decimal("0")
    TempSum = Decimal('0')
    try:
        Amount = Decimal(Req.REQUEST.get("amount", None))
        Query = "SELECT * FROM main_ordersmem  WHERE  currency1=%i AND currency2=%i \
                          AND status='processing'  \
                          AND user!=%i  ORDER BY price DESC" % (
            CurrentTradePair.currency_on.id,
            CurrentTradePair.currency_from.id,
            Req.user.id)
        List = OrdersMem.objects.raw(Query)
        for item in List:
            if Amount > item.sum1:
                Amount -= item.sum1
                TempSum += item.sum1
                SumList.append({"sum": item.sum1, "price": item.price})
            else:
                TempSum += Amount
                SumList.append({"sum": Amount, "price": item.price})
                break
    except:
        Response = HttpResponse('{"status":false, "description":"amount is incorrect"}')
        Response['Content-Type'] = 'application/json'
        return Response
        # format_numbers_strong(balance_buy.balance )

    AvaragePrice = Decimal("0")
    BuySum = Decimal("0")
    for item in SumList:
        BuySum += item['sum']
        AvaragePrice += ((item['sum'] / TempSum) * item['price'] )
    Dict = {"buy_sum": format_numbers_strong(BuySum),
            "price": format_numbers_strong(AvaragePrice),
            "status": True}
    RespJ = json.JSONEncoder().encode(Dict)
    return cached_json_object(RespJ)


@my_cache
def buy_list(Req, Pair):
    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Pair)
    except:
        return json_false500(Req)

    BuyList = OrdersMem.objects.filter(status="processing",
                                       currency1=Current.currency_from.id,
                                       currency2=Current.currency_on.id)
    getcontext().prec = settings.TRANS_PREC
    Currency1Title = Current.currency_from.title
    Currency2Title = Current.currency_on.title
    List1 = {}
    AccumBuySum = 0
    for item in BuyList:
        SellSum = item.sum1  ## UAH
        BuySum = item.sum2  ## LTC
        Rate = item.price
        AccumBuySum += SellSum
        if List1.has_key(Rate):
            List1[Rate][Currency1Title] = List1[Rate][Currency1Title] + SellSum
            List1[Rate][Currency2Title] = List1[Rate][Currency2Title] + BuySum
        else:
            List1[Rate] = {Currency1Title: SellSum, Currency2Title: BuySum}

    ResBuyList = []

    LL = List1.keys()
    L = []
    for i in LL:
        Temp = Decimal(i)
        List1[Temp] = List1[i]
        L.append(Temp)

    L.sort()
    L.reverse()

    Price = 0
    MaxPrice = 0
    for i in L:
        Price = format_numbers10(i)
        ResBuyList.append({"price": Price,
                           "currency_trade": format_numbers10(List1[i][Currency2Title]),
                           "currency_base": format_numbers10(List1[i][Currency1Title])})

    if len(ResBuyList):
        MaxPrice = ResBuyList[0]["price"]
    Dict = {"orders_sum": format_numbers10(AccumBuySum), "list": ResBuyList,
            "max_price": MaxPrice, "min_price": Price}
    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


@json_auth_required
def order_status(Req, Id):
    Dict = {}
    try:
        order = Orders.objects.get(id=int(Id), user=Req.user)
        Dict["pub_date"] = str(order.pub_date)
        Dict["sum1"] = str(order.sum1)
        Dict["id"] = str(Id)
        Dict["sum2"] = str(order.sum2)
        Dict["sum1_history"] = str(order.sum1_history)
        Dict["sum2_history"] = str(order.sum2_history)
        Dict["currency1"] = order.currency1.title
        Dict["currency2"] = order.currency1.title
        Dict["status"] = order.status
    except Orders.DoesNotExist:
        return status_false()
    Response = HttpResponse(json.JSONEncoder().encode(Dict))
    Response['Content-Type'] = 'application/json'
    return Response


@my_cache
def balance(Req, User_id):
    List = []
    Dict = {}
    for i in Accounts.objects.filter(user_id=User_id):
        List.append({"balance": format_numbers10(i.balance), "currency": i.currency.title})

    User = Req.user
    Dict["notify_count"] = Msg.objects.filter(user_to=User,
                                              user_from_id=1,
                                              user_hide_to="false",
                                              user_seen_to="false").count()
    Dict["msg_count"] = Msg.objects.filter(user_to=User,
                                           user_hide_to="false",
                                           user_seen_to="false").exclude(user_from_id=1).count()
    try:
        online = OnlineUsers(user=Req.user)
        online.save()
    except:
        online = OnlineUsers.objects.get(user=Req.user)
        online.pub_date = datetime.datetime.now()
        online.save()

    if Req.session.has_key('use_f2a'):
        Dict["use_f2a"] = Req.session['use_f2a']
    else:
        Dict["use_f2a"] = False

    Dict["accounts"] = List
    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


@json_auth_required
def user_balance(Req):
    return balance(Req, Req.user.id)

    # Dict["accounts"] = []
    # Response =  HttpResponse( json.JSONEncoder().encode(Dict) )
    # Response['Content-Type'] = 'application/json'
    # return Response


@my_cache
def sell_list(Req, Pair):
    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Pair)
    except:
        return json_false500(Req)

    SellList = OrdersMem.objects.filter(status="processing",
                                        currency1=Current.currency_on.id,
                                        currency2=Current.currency_from.id)
    getcontext().prec = 8
    Currency1Title = Current.currency_from.title
    Currency2Title = Current.currency_on.title
    AccumSellSum = 0
    GroupSellDict = {}
    for item in SellList:
        SellSum = item.sum1  ##LTC
        BuySum = item.sum2  ## UAH
        Rate = item.price
        AccumSellSum += SellSum
        if GroupSellDict.has_key(Rate):
            GroupSellDict[Rate][Currency2Title] = GroupSellDict[Rate][Currency2Title] + SellSum
            GroupSellDict[Rate][Currency1Title] = GroupSellDict[Rate][Currency1Title] + BuySum
        else:
            GroupSellDict[Rate] = {Currency2Title: SellSum, Currency1Title: BuySum}

    ResSellList = []
    LL = GroupSellDict.keys()
    L = []
    for i in LL:
        Temp = Decimal(i)
        GroupSellDict[Temp] = GroupSellDict[i]
        L.append(Temp)

    L.sort()

    Price = 0
    MinPrice = 0
    for i in L:
        Price = format_numbers10(i)
        ResSellList.append({"price": Price,
                            "currency_trade": format_numbers10(GroupSellDict[i][Currency2Title]),
                            "currency_base": format_numbers10(GroupSellDict[i][Currency1Title])})

    if len(ResSellList):
        MinPrice = ResSellList[0]["price"]

    Dict = {"orders_sum": format_numbers10(AccumSellSum),
            "list": ResSellList,
            "min_price": MinPrice,
            "max_price": Price}
    RespJ = json.JSONEncoder().encode(Dict)

    return RespJ


@my_cache
def last_price(Req, Pair):
    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Pair)
    except:
        return json_false500(Req)
    Dict = None
    try:
        deal = DealsMemory.objects.filter(trade_pair=Current.id).latest("id")
        Dict = {"price": format_numbers4(deal.price), "price_10": format_numbers10(deal.price)}
    except:
        Dict = {"price": "0", "price_10": "0.000000000"}

    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


### TODO stat
@my_cache
def day_stat(Req, Pair):
    Current = TradePairs.objects.get(url_title=Pair)
    ##last value 17520
    cursor = connection.cursor()
    Q = cursor.execute("SELECT 	  sum(VolumeTrade) as VolumeTrade, \
                                  sum(VolumeBase) as VolumeBase,\
                                  max(Max) as Max,\
                                  min(Min) as Min \
                                  FROM main_stockstat WHERE  main_stockstat.Stock_id=%i \
                                  ORDER BY id DESC LIMIT  17520 " % Current.id)

    List = dictfetchall(cursor, Q)
    row = List[0]
    for i in row:
        if not row[i]:
            row[i] = format_numbers4(Decimal("0"))
        else:
            row[i] = format_numbers4(Decimal(row[i]))

    Dict = {"volume_base": row['VolumeBase'],
            "volume_trade": row['VolumeTrade'],
            "min": row['Min'],
            "max": row['Max'],
    }

    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


@my_cache
def high_japan_stat(Req, Pair):
    Current = TradePairs.objects.get(url_title=Pair)
    # last value 17520
    List = StockStat.objects.raw("SELECT * FROM main_stockstat WHERE  main_stockstat.Stock_id=%i \
                                  ORDER BY id DESC LIMIT  17520 " % Current.id)
    ListJson = []
    VolumeBase = 0
    VolumeTrade = 0
    i = 0
    for item in List:
        StartDate = item.start_date
        if i < 48:
            VolumeTrade = VolumeTrade + item.VolumeTrade
            VolumeBase = VolumeBase + item.VolumeBase
        i += 1
        Key = calendar.timegm(StartDate.utctimetuple())
        ListJson.append([int(Key) * 1000, float(item.Start), float(item.Max), float(item.Min), float(item.End),
                         float(item.VolumeTrade)])

    OnlineUsersCount = OnlineUsers.objects.count()
    ListJson.reverse()

    Dict = {"trades": ListJson,
            "online": OnlineUsersCount,
            "volume_base": str(VolumeBase),
            "volume_trade": str(VolumeTrade)}

    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


@my_cache
def japan_stat(Req, Pair):
    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Pair)
    except:
        return json_false500(Req)

    List = StockStat.objects.raw("SELECT * FROM main_stockstat WHERE  main_stockstat.Stock_id=%i \
                                  ORDER BY id DESC LIMIT 48 " % Current.id)
    ListJson = []
    VolumeBase = 0
    VolumeTrade = 0
    for item in List:
        StartDate = item.start_date
        VolumeTrade = VolumeTrade + item.VolumeTrade
        VolumeBase = VolumeBase + item.VolumeBase
        Key = "%i:%i" % (StartDate.hour, StartDate.minute)
        ListJson.append(
            [Key, float(item.Start), float(item.Max), float(item.Min), float(item.End), float(item.VolumeTrade)])

    OnlineUsersCount = OnlineUsers.objects.count()
    ListJson.reverse()

    Dict = {"trades": ListJson,
            "online": OnlineUsersCount,
            "volume_base": str(VolumeBase),
            "volume_trade": str(VolumeTrade)}

    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


##TODO add date filters
@my_cache
def deal_list(Req, Pair):
    ResList = common_deal_list(Pair)
    JsonP = json.JSONEncoder().encode(ResList)
    return JsonP


def common_deal_list(Pair, User_id=None):
    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Pair)
    except:
        return json_false500(Req)

    ldeals = None
    if User_id is None:
        ldeals = DealsMemory.objects.filter(trade_pair=Current.id).order_by("-id")
    else:
        ldeals = DealsMemory.objects.filter(trade_pair=Current.id, user_id=User_id).order_by("-id")

    ResList = []
    for item in ldeals:
        new_item = {}
        rate = item.price
        new_item['pub_date'] = formats.date_format(item.pub_date, "DATETIME_FORMAT")
        new_item["type"] = item.type_deal
        new_item["user"] = item.user
        new_item["price"] = format_numbers10(rate)
        new_item["amnt_base"] = format_numbers10(item.amnt_base)
        new_item["amnt_trade"] = format_numbers10(item.amnt_trade)
        ResList.append(new_item)

    return ResList


@json_auth_required
def my_closed_orders(Req, Pair):
    ResList = common_deal_list(Pair, Req.user.id)
    Response = HttpResponse(json.JSONEncoder().encode(ResList))
    Response['Content-Type'] = 'application/json'
    return Response


@my_cache
def client_orders(Req, User_id, Title):
    Dict = {}

    Current = None
    try:
        Current = TradePairs.objects.get(url_title=Title)
    except:
        return json_false500(Req)

    Dict["auth"] = True
    MyOrders = OrdersMem.objects.raw("SELECT * FROM main_ordersmem WHERE user=%i AND ( \
                                        (currency1=%i AND currency2=%i ) OR  \
                                        (currency2=%i AND currency1=%i )\
                                        ) AND status='processing' ORDER BY id DESC" %
                                     (User_id,
                                      Current.currency_from.id,
                                      Current.currency_on.id,
                                      Current.currency_from.id,
                                      Current.currency_on.id,
                                     )
    )

    MyOrdersList = []
    c = getcontext()
    c.prec = settings.TRANS_PREC

    for i in MyOrders:
        MyOrdersDict = {}
        MyOrdersDict["pub_date"] = formats.date_format(i.pub_date, "DATETIME_FORMAT")
        MyOrdersDict["id"] = i.id
        MyOrdersDict["sum2"] = str(i.sum2)
        MyOrdersDict["sum1"] = str(i.sum1)

        if i.currency1 == Current.currency_on.id:
            MyOrdersDict["type"] = "sell"
            Number = i.sum2 / i.sum1
            MyOrdersDict["price"] = format_numbers10(i.price)
            MyOrdersDict["amnt_trade"] = format_numbers10(i.sum1)
            MyOrdersDict["amnt_base"] = format_numbers10(i.sum2)
        else:
            MyOrdersDict["type"] = "buy"
            Number = i.sum1 / i.sum2
            MyOrdersDict["price"] = format_numbers10(i.price)
            MyOrdersDict["amnt_base"] = format_numbers10(i.sum1)
            MyOrdersDict["amnt_trade"] = format_numbers10(i.sum2)
        MyOrdersList.append(MyOrdersDict)

    balance_sell = Accounts.objects.get(user_id=User_id, currency=Current.currency_on)
    balance_buy = Accounts.objects.get(user_id=User_id, currency=Current.currency_from)
    Dict["balance_buy"] = format_numbers_strong(balance_buy.balance)
    Dict["balance_sell"] = format_numbers_strong(balance_sell.balance)
    Dict["your_open_orders"] = MyOrdersList
    RespJ = json.JSONEncoder().encode(Dict)
    return RespJ


@json_auth_required
def my_orders(Req, Title):
    return client_orders(Req, Req.user.id, Title)
        
        




     



