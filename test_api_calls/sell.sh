#!/bin/sh

curl -k   -i -H "api_sign: 652167fcdc3d0f55cacd4f2eea27e2f2512669126b2ddf5b5cbdbd8e18c23592" -H "public_key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38"  --data "currency1=UAH&currency=BTC&count=0.003&price=6200&out_order_id=4&nonce=4" -v https://ttt.btc-trade.com.ua/api/sell/btc_uah
