import logging

# from tornaduv import UVLoop
import tornado.web
# import tornaduv
# import pyuv
import threading
from crypton.http import MemStore
import json

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


@json_request
@checkout_auth
def checkout(req):
    resp_format = req["format"]
    req_data =  req["data"]
    public_id  = req_data["public_id"]
    (addr, ref) = get_avalible_adress(public_id)
    (amount, price) = calculate_btc_amount(req_data["amount"])
    (moment_amount, price_moment) = calculate_btc_amount4momentory(req_data["amount"])
    resp_dict = {
        "ref": ref,
        "amount": amount,
        "price": price,
        "amount_moment": moment_amount,
        "price_moment": price_moment,
        "addr": addr,
        "invoice_data": req_data
    }
    if resp_format == "json":
        return json_response(resp_dict)

    return invoice_html(resp_dict)







