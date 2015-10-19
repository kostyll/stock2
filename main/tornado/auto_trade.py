# account buyer, sum to buy, item - order seller, Order - order buyer
def create_order(User, Amnt1, Amnt2, Currency1, Currency2, TradePair, Status="created"):
    if TradePair.currency_on.id == Currency1.id:
        transit1 = TradePair.transit_on
        transit2 = TradePair.transit_from
    else:
        transit2 = TradePair.transit_on
        transit1 = TradePair.transit_from

    order = Orders(user=User,
                   currency1=Currency1,
                   currency2=Currency2,
                   sum1_history=Amnt1,
                   sum2_history=Amnt2,
                   sum1=Amnt1,
                   sum2=Amnt2,
                   transit_1=transit1,
                   transit_2=transit2,
                   trade_pair=TradePair,
                   status=Status
    )
    order.save()
    return order


def deposit_funds(Order):
    return _("Deposit funds  %(sum)s %(currency)s according with order #%(order_id)i " % {
        'sum': Order.sum1_history,
        'currency': Order.currency1.title,
        'order_id': Order.id})


def order_finish(Order):
    return _("You order #%(order_id)i is fully completed" % {'order_id': Order.id})


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


def order_return_unused(Order, Currency1, AccumSumToSell):
    return _("Return %(sum).8f %(currency)s unused funds according with order #%(order_id)i  " %
             {'sum': AccumSumToSell,
              'currency': str(Currency1),
              'order_id': Order.id})


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


# AccumSum2Buy, AccumSumToSell
def process_order(AccountBuyer, ComisBuy, AccumSum, AccumSumToSell, item, Order, TradePair, ComisSell):
    ##TODO move to settings for every user
    ComisPercentSeller = item.comission
    ComisPercentBuyer = Order.comission

    if not item.verify(str(item.user)):
        ##TODO add warning logging
        return (AccumSum, AccumSumToSell)

    if item.sum1 > AccumSum:
        ## a danger of low overflow
        Diff = AccumSum / item.sum1
        TransSum = item.sum2 * Diff
        #TransSum = AccumSumToSell
        AccountSeller = get_account(item.user, item.currency2)
        ##comission
        item.sum1 = item.sum1 - AccumSum
        item.sum2 = item.sum2 - TransSum
        item.sign_record(str(item.user))
        item.save()

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
            system_notify(order_description_sell(AccumSum, TransSum, item, TradePair), AccountSeller.user.id)
            system_notify(order_description_buy(TransSum, AccumSum, Order, item, TradePair), AccountBuyer.user.id)
        except:
            pass

        return (0, AccumSumToSell - TransSum)

    if item.sum1 <= AccumSum:

        TransSum = item.sum2
        NotifySum = item.sum1
        AccountSeller = get_account(item.user, item.currency2)
        ##comission
        # TODO move to archive
        item.status = "processed"
        item.save()
        item.sum1 = 0
        item.sum2 = 0

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

        item.make2processed()

        try:
            system_notify(order_description_sell(NotifySum, TransSum, item, TradePair), AccountSeller.user.id)
            system_notify(order_description_buy(TransSum, NotifySum, Order, item, TradePair), AccountBuyer.user.id)
            system_notify(order_finish(item), AccountSeller.user.id)
        except:
            pass

        return (AccumSum - NotifySum, AccumSumToSell - TransSum )


def make_auto_trade(Order, TradePair, Price, Currency1, Sum1, Currency2, Sum2):
    List = None
    ##if we sell
    #Query = "SELECT * FROM main_ordersmem  WHERE  trade_pair_id=%i" % (TradePair.id)

    if int(TradePair.currency_on.id) == int(Currency1.id):
        Query = "SELECT * FROM main_ordersmem  WHERE  currency1=%i AND currency2=%i \
                           AND status='processing' AND price >= %s  \
                           AND user!=%i  ORDER BY price DESC" % (Currency2.id,
                                                                 Currency1.id,
                                                                 format_numbers_strong(Price), Order.user)
    else:
        Query = "SELECT * FROM main_ordersmem WHERE  currency1=%i AND currency2=%i \
                           AND status='processing' AND price <= %s \
                           AND user!=%i  ORDER BY price " % (Currency2.id,
                                                             Currency1.id,
                                                             format_numbers_strong(Price), Order.user )

    List = OrdersMem.objects.raw(Query)

    ##work on first case
    CommissionSell = Accounts.objects.get(user_id=settings.COMISSION_USER, currency=Currency1)
    ComnissionBuy = Accounts.objects.get(user_id=settings.COMISSION_USER, currency=Currency2)
    AccumSumToSell = Sum1
    AccumSum2Buy = Sum2
    AccountBuyer = get_account(Order.user, Currency2.id)
    UserDeals = [Order.user]
    for item in List:
        (AccumSum2Buy, AccumSumToSell ) = process_order(AccountBuyer, ComnissionBuy, AccumSum2Buy,
                                                        AccumSumToSell, item, Order,
                                                        TradePair, CommissionSell)
        UserDeals.append([item.user])
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

    else:
        Order.save()

    return {"start_sum": Sum2, "last_sum": ResultSum, "users_bothered": UserDeals}


def return_rest2acc(Order, AccumSumToSell):
    Account2Sell = get_account(Order.user, Order.currency1)
    add_trans2(Order.transit_1,
               AccumSumToSell,
               Order.currency1,
               Account2Sell.id,
               Order.id,
               "deal_return")
    system_notify(order_return_unused(Order, Account2Sell.currency, AccumSumToSell), Order.user)


def finish_create_order(TradePair, SumToBuy, AccumSumToSell, Order):
    ##base currency
    if Order.currency1 == TradePair.currency_on:

        if AccumSumToSell < TradePair.min_trade_base:
            system_notify(order_finish(Order), Order.user)
            return 0
        else:
            return SumToBuy
    else:
        if SumToBuy < TradePair.min_trade_base:
            system_notify(order_finish(Order), Order.user)
            return 0
        else:
            return SumToBuy


def process_auto(Req, Res, TradePair):
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

    DeleteKeys = []
    cache = caching()
    Type = TradePair.url_title
    for i in Res["users_bothered"]:
        CachedKey1 = 'client_orders_' + str(i) + "_" + Type
        CachedKey2 = 'balance_' + str(i)
        DeleteKeys.append(CachedKey1)
        DeleteKeys.append(CachedKey2)
    #deal_list_btc_uah
    DeleteKeys.append("deal_list_" + Type)
    DeleteKeys.append("sell_list_" + Type)
    DeleteKeys.append("buy_list_" + Type)

    cache.delete_many(DeleteKeys)

    return Encoder.encode(Dict)