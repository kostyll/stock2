from main.models import TradePairs
from main.models import Accounts, AccountsAdmin
from main.models import Trans, TransAdmin

from main.models import TransMem, TransMemAdmin
from main.models import TransIn, TransInAdmin
from main.models import TransOut, TransOutAdmin

from main.models import Orders, OrdersAdmin
from main.models import OrdersMem, OrdersMemAdmin
from main.models import MsgAdmin, Msg, StaticPage, StaticPageAdmin
from main.models import BankTransfersAdmin, BankTransfers
from main.models import Chat, ChatHistory
from main.models import CryptoTransfers, CryptoTransfersAdmin
from main.models import LiqPayTransAdmin, LiqPayTrans
from main.models import StockStatAdmin, StockStat
from main.models import CardP2PTransfers, CardP2PTransfersAdmin
from main.models import HoldsWithdraw
from main.models import CustomMetaHackAdmin, CustomMetaHack
from main.models import OnlineUsers, OnlineUsersAdmin
from main.models import CustomMailAdmin, CustomMail
from main.models import VolatileConsts, Category
from main.models import MyUserAdmin
from django.contrib.auth.models import User
from main.models import VolatileConsts
from main.models import CustomMailMultiAdmin, CustomMailMulti
from main.models import PinsImages, PinsImagesAdmin

from main.models import PartnershipAdmin, Partnership
from django.contrib import admin

from main.models import OrderTimerAdmin, OrderTimer
from main.models import UserCustomSettings, UserCustomSettingsAdmin
from main.models import CustomSettings, CustomSettingsAdmin
from main.models import CurrencyAdmin, Currency
from main.models import P24TransIn, OutRequest, ObjectionsP2P, P24TransInAdmin
from main.models import btce_trade_stat_minute_usd, btce_trade_stat_minute_usdAdmin
from main.models import Balances, ResetPwdLink

from main.models import NewsPageAdmin, NewsPage

admin.site.disable_action('delete_selected')
admin.site.register(TransIn, TransInAdmin)
admin.site.register(TransOut, TransOutAdmin)
admin.site.register(NewsPage, NewsPageAdmin)

admin.site.register(Partnership, PartnershipAdmin)
admin.site.register(OrderTimer, OrderTimerAdmin)
admin.site.register(PinsImages, PinsImagesAdmin)
admin.site.register(Balances)
admin.site.register(P24TransIn, P24TransInAdmin)
admin.site.register(OutRequest)
admin.site.register(ObjectionsP2P)
admin.site.register(ResetPwdLink)
admin.site.register(Category)

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(btce_trade_stat_minute_usd, btce_trade_stat_minute_usdAdmin)
admin.site.register(CustomMailMulti, CustomMailMultiAdmin)

admin.site.register(CustomSettings, CustomSettingsAdmin)

admin.site.register(UserCustomSettings, UserCustomSettingsAdmin)

admin.site.register(VolatileConsts)

admin.site.unregister(User)

admin.site.register(User, MyUserAdmin)

admin.site.register(CustomMail, CustomMailAdmin)

admin.site.register(CardP2PTransfers, CardP2PTransfersAdmin)

admin.site.register(CustomMetaHack, CustomMetaHackAdmin)

admin.site.register(StaticPage, StaticPageAdmin)

admin.site.register(StockStat, StockStatAdmin)

admin.site.register(BankTransfers, BankTransfersAdmin)

admin.site.register(CryptoTransfers, CryptoTransfersAdmin)

admin.site.register(ChatHistory)

admin.site.register(Chat)

admin.site.register(HoldsWithdraw)

admin.site.register(OnlineUsers, OnlineUsersAdmin)

admin.site.register(TradePairs)

admin.site.register(Msg, MsgAdmin)

admin.site.register(LiqPayTrans, LiqPayTransAdmin)

admin.site.register(Accounts, AccountsAdmin)

admin.site.register(Trans, TransAdmin)
admin.site.register(TransMem, TransMemAdmin)

admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrdersMem, OrdersMemAdmin)

