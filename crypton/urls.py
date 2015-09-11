from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from crypton import settings


    
urlpatterns = patterns('',
    # Examples:
    url(r'^project/banner/(\w+)$', 'main.banners.banner', name='banner'),
    url(r'^robots.txt$', 'main.views.robots', name='robots'),
    url(r'^time$', 'main.views.time', name='time'),
    url(r'^sitemap.xml$', 'main.views.sitemap', name='sitemap'),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^public/balance$', 'main.views.crypto_balances_home', name='crypto_balances_home'),      
    url(r'^public/balance/([\w]+)$', 'main.views.crypto_balances', name='crypto_balances'),      
    url(r'^stock/([\w]+)$', 'main.views.stock', name='stock'),
    url(r'^stock$', 'main.views.stock', name='stock'),
    
    url(r'^profile/common_secure_page/private_key$', 'main.profile.page_private_key', name='page_private_key'),   
    url(r'^profile/private_key$', 'main.profile.private_key', name='private_key'),   
    url(r'^profile/settings/g2a/no$', 'main.profile.g2a_turn_off', name='g2a_turn_off'),   
    url(r'^profile/settings/([\w]+)/([\w]+)$', 'main.profile.user_settings', name='user_settings'),        
    url(r'^profile/reset$', 'main.profile.reset', name='reset'),
    url(r'^profile/pin_change_do$', 'main.profile.pin_change_do', name='pin_change_do'),    
    url(r'^profile/pin_change$', 'main.profile.pin_change', name='pin_change'),    
    url(r'^profile/qr$', 'main.profile.g2a_qr', name='g2a_qr'),    
    url(r'^profile/setup_g2a_verify/([\w]+)$', 'main.profile.setup_g2a_verify', name='setup_g2a_verify'),    
    url(r'^profile/setup_g2a$', 'main.profile.setup_g2a', name='setup_g2a'),    
    url(r'^profile$', 'main.profile.profile', name='profile'),      

    
    url(r'^pin_image_page/([\w]+)$', 'main.profile.pin_image_page', name = 'pin_image_page'),
    
    url(r'^pin_image/([\w]+)$', 'main.profile.pin_image', name = 'pin_image'),
    
    url(r'^profile/([\w]+)$', 'main.profile.profile', name='profile'),
    
    url(r'^msgs$', 'main.msgs.msgs_in', name='msgs_in'),
    url(r'^msgs/in$', 'main.msgs.msgs_in', name='msgs_in'),
    url(r'^msgs/out$', 'main.msgs.msgs_out', name='msgs_out'),
    url(r'^msgs/create$', 'main.msgs.create', name='create'),
    
    url(r'^msgs/hide/([\w]+)$', 'main.msgs.hide', name='hide'),
    url(r'^page/help$', 'main.views.page_help', name='page_help'),   
    
    url(r'^page/([\w]+)$', 'main.views.page', name='page'),   
    url(r'^page_discuss/([\w]+)$', 'main.views.page_discuss', name='page_discuss'),   
    url(r'^notification$', 'main.msgs.notification', name='notification'),
    url(r'^logout$', 'main.views.try_logout', name='try_logout'),
    url(r'^login_page$', 'main.views.login_page', name='login_page'),
    url(r'^login$', 'main.views.try_login', name='try_login'),
    url(r'^login_f2a$', 'main.views.login_f2a', name='login_f2a'),
    url(r'^login_f2a_operation$', 'main.views.login_f2a_operation', name='login_f2a_operation'),
    url(r'^user_panel/([\w]+)$', 'main.views.user_panel', name='user_panel'),
    url(r'^registration/([\w]+)$', 'main.views.registration_ref', name='registration_ref'),
    url(r'^registration$', 'main.views.registration', name='registration'),

    url(r'^try_regis$', 'main.views.try_regis', name='try_regis'),
    url(r'^regis_success', 'main.views.regis_success', name='regis_success'),
    url(r'^fin_regis/([\w]+)', 'main.views.fin_regis', name='fin_regis'),

    # forgot_password_views
    url(r'^forgot$', 'main.forgot_password_views.forgot', name='forgot'),
    url(r'^forgot_action$', 'main.forgot_password_views.forgot_action', name='forgot_action'),
    url(r'^forgot_success$', 'main.forgot_password_views.forgot_success', name='forgot_success'),
    url(r'^reset_pwd_action/([\w]+)$', 'main.forgot_password_views.reset_pwd_action', name='reset_pwd_action'),
    url(r'^reset_pwd/([\w]+)$', 'main.forgot_password_views.reset_pwd', name='reset_pwd'),
    url(r'^reset_link_no_found$', 'main.forgot_password_views.reset_link_no_found', name='reset_link_no_found'),
    url(r'^reset_success', 'main.forgot_password_views.reset_success', name='reset_success'),

    




    url(r'^api/market_prices',  'main.api.market_prices', name='market_prices'),
    url(r'^api/japan_stat/high/([\w]+)',  'main.api.high_japan_stat', name='japan_stat'),
    url(r'^api/japan_stat/([\w]+)',  'main.api.japan_stat', name='japan_stat'),
    url(r'^api/trades/buy/([\w]+)',  'main.api.buy_list', name='buy_list'),
    url(r'^api/trades/sell/([\w]+)',  'main.api.sell_list', name='sell_list'),
    url(r'^api/buy/([\w]+)',  'main.api.buy', name='buy'),

    url(r'^api/auth',  'main.api.auth', name='auth'),
    url(r'^api/ask/([\w]+)',  'main.api.ask', name='ask'),
    url(r'^api/bid/([\w]+)',  'main.api.bid', name='bid'),
    
    url(r'^api/sell/([\w]+)',  'main.api.sell', name='sell'),
    url(r'^api/remove/order/([\w]+)', 'main.api.remove_order', name='remove_order'),
    url(r'^api/my_orders/([\w]+)', 'main.api.my_orders', name='my_orders'),
    url(r'^api/order/status/([\w]+)', 'main.api.order_status', name='order_status'),
    url(r'^api/deals/([\w]+)', 'main.api.deal_list', name='deal_list'),


    url(r'^api/balance', 'main.api.user_balance', name='user_balance'),
    url(r'^api/my_deals/([\w]+)', 'main.api.my_closed_orders', name='my_closed_orders'),


    url(r'^finance/bank_transfer/UAH/([\w\.]+)',
         'main.finance.bank_deposit', 
         name='bank_deposit'),
    
    url(r'^finance/crypto_currency/([\w\.]+)',
        'main.finance.crypto_currency_get_account', 
        name='crypto_currency_get_account' ),
    
    
    
    url(r'^finance/refs$', 'main.finance.refs', name='refs' ),

    url(r'^finance/depmotion/([\w]+)', 'main.finance.depmotion', name='depmotion' ),

    url(r'^finance/depmotion', 'main.finance.depmotion_home', name='depmotion_home' ),

    url(r'^finance/liqpay/deposit/([\w\.]+)', 'main.finance.liqpay_deposit', name='liqpay_deposit' ),
    url(r'^finance/liqpay/start/([\w\.]+)', 'main.finance.liqpay_start_pay', name='liqpay_start_pay' ),    
    
    
    url(r'^finance/p24/deposit/([\w\.]+)', 'main.finance.p24_deposit', name='p24_deposit' ),
    url(r'^finance/p24/start/([\w\.]+)', 'main.finance.p24_start_pay', name='p24_start_pay' ),    
    url(r'^finance/p24/hui_hui_hui/([\w]+)', 'main.finance.p24_call_back_url', name='p24_call_back_url' ), 
    
    url(r'^finance/perfectmoney/deposit/([\w]+)/([\w\.]+)', 'main.finance_perfect.perfect_deposit', name='perfect_deposit' ),
    url(r'^finance/perfectmoney/start/([\w]+)/([\w\.]+)', 'main.finance_perfect.perfect_start_pay', name='perfect_start_pay' ),    
    url(r'^finance/perfectmoney/hui_hui_hui/([\w]+)/([\w\.]+)', 'main.finance_perfect.perfect_call_back_url', name='perfect_call_back_url' ), 
    url(r'^finance/perfectmoney/hui_hui_hui_hui/([\w]+)', 'main.finance_perfect.perfect_call_back_url_fail', name='perfect_call_back_url_fail' ), 
    
    url(r'^finance/okpay/deposit/([\w]+)/([\w\.]+)', 'main.okpay.deposit', name='okpay_deposit' ),
    url(r'^finance/okpay/start/([\w]+)/([\w\.]+)', 'main.okpay.start_pay', name='okpay_start_pay' ),    
    url(r'^finance/okpay/hui_hui_hui/([\w]+)', 'main.okpay.call_back_url', name='call_back_url' ), 
    
    url(r'^finance/payeer/deposit/([\w]+)/([\w\.]+)', 'main.payeer.deposit', name='payeer_deposit' ),
    url(r'^finance/payeer/start/([\w]+)/([\w\.]+)', 'main.payeer.start_pay', name='payeer_start_pay' ),    
    url(r'^finance/payeer/hui_hui_hui/([\w]+)/([\w\.]+)', 'main.payeer.call_back_url', name='payeer_call_back_url' ), 
    url(r'^finance/payeer/hui_hui_hui_hui/([\w]+)', 'main.payeer.call_back_url', name='call_back_url' ), 
    
    url(r'^finance/ya/deposit/([\w]+)/([\w\.]+)', 'main.ya.deposit', name='ya_deposit' ),
    url(r'^finance/ya/start/([\w]+)/([\w\.]+)', 'main.ya.start_pay', name='ya_start_pay' ),    
    url(r'^finance/ya/hui_hui_hui', 'main.ya.call_back_url', name='ya_call_back_url' ), 
 
    
    
    url(r'^finance/trans$', 'main.finance.trans', name='trans' ),
    
    
    url(r'^finance/open_orders/([\w]+)', 'main.finance.open_orders', name='open_orders' ),
    url(r'^finance/deals/([\w]+)', 'main.finance.deals', name='deals' ),
    
    url(r'^finance/common_confirm_page/([\w]+)', 'main.finance.common_confirm_page', name='common_confirm_page' ),
    
    url(r'^finance/liqpay/hui_hui_hui/([\w]+)', 'main.finance.liqpay_call_back_url', name='call_back_url' ), 
            
    url(r'^finance/common_secure_page/([\w]+)/([\w]+)$','main.finance.common_secure_page', 
                name='common_secure_page'),
    
    url(r'^finance/common_secure_confirm$','main.finance.common_secure_confirm', 
                name='common_secure_confirm'),
    
    url(r'^finance/liqpay_transfer_withdraw/([\w]+)/([\w\.]+)','main.finance.liqpay_transfer_withdraw', 
                name='liqpay_transfer_withdraw'),
                
    url(r'^finance/perfect_transfer_withdraw/([\w]+)/([\w\.]+)','main.finance_perfect.perfect_transfer_withdraw', 
                name='perfect_transfer_withdraw'),  
                
    url(r'^finance/okpay_transfer_withdraw/([\w]+)/([\w\.]+)','main.finance.okpay_transfer_withdraw', 
                name='okpay_transfer_withdraw'),
    
                
    
    url(r'^finance/liqpay_transfer_withdraw_submit$','main.finance.liqpay_transfer_withdraw_submit', 
                name='liqpay_transfer_withdraw_submit'),
   
    url(r'^finance/p2p_transfer_withdraw/([\w]+)/([\w\.]+)','main.finance.p2p_transfer_withdraw', 
                name='p2p_transfer_withdraw'),
    
    url(r'^finance/p2p_transfer_withdraw_submit$','main.finance.p2p_transfer_withdraw_submit', 
                name='p2p_transfer_withdraw_submit'),
    
    url(r'^finance/bank_transfer_withdraw/([\w]+)/([\w\.]+)','main.finance.bank_transfer_withdraw', 
                name='bank_transfer_withdraw' ),
    
    url(r'^finance/bank_transfer_withdraw_submit$','main.finance.bank_transfer_withdraw_submit', 
                name='bank_transfer_withdraw_submit'),    
    url(r'^finance/crypto_transfer_withdraw/([\w]+)','main.finance.crypto_currency_withdraw', 
                name='crypto_currency_withdraw'),
    url(r'^finance/crypto_currency_withdraw_submit','main.finance.crypto_currency_withdraw_submit', 
                name='crypto_currency_withdraw_submit'),
                
    url(r'^set_lang/([\w]+)','main.views.set_lang', name='set_lang'),
    
    
    #url(r'^finance/confirm_withdraw_bank/([\w]+)$', 
        #'main.finance.confirm_withdraw_bank', name='confirm_withdraw_bank' ),
    #url(r'^finance/confirm_withdraw_liqpay/([\w]+)$',
        #'main.finance.confirm_withdraw_liqpay', name='confirm_withdraw_liqpay' ),
    #url(r'^finance/confirm_withdraw_currency/([\w]+)$', 
        #'main.finance.confirm_withdraw_currency', name='confirm_withdraw_currency' ),
    #url(r'^finance/confirm_withdraw_p2p/([\w]+)$',
        #'main.finance.confirm_withdraw_p2p',
        #name='confirm_withdraw_p2p' ),
    
    
    url(r'^foreign/stock/btce/([\w]+)/minute/([\d]+)$', 'main.stock.btce_btc_usd', name='stock'),
    

    url(r'^finance/confirm_withdraw_msg$',
        'main.finance.confirm_withdraw_msg',
        name='confirm_withdraw_msg' ), 
    url(r'^finance/confirm_withdraw_msg_auto',
        'main.finance.confirm_withdraw_msg_auto',
        name='confirm_withdraw_msg_auto' ),    
        
    url(r'^finance', 'main.finance.home', name='home' ),
   
  
    #url(r'^crypton/', include('crypton.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^captcha/', include('captcha.urls')),  
    #(r'^support/', include('helpdesk.urls')),
    url(r'^admin/main/whole_balance$', 'main.admin_reports.whole_balance', name="whole_balance"),
    #url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^tinymce/', include('tinymce.urls')),    
    #url(r'^img/(?P<path>.*)$', 'django.views.static.serve',         
    # {'document_root': settings.MEDIA_ROOT}),
    #{'document_root': settings.STATIC_ROOT, 'show_indexes': True})
)


handler500 = 'main.views.my_custom_error_view'

        
       
        



