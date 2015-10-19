from jsonrpc import ServiceProxy
from sdk.crypto_settings import Settings


class CryptoAccount:
    def __init__(self, currency="BTC", account=None):
        self.__host = Settings[currency]["host"]
        self.__port = Settings[currency]["port"]
        self.__account = account
        self.__rpc_user = Settings[currency]["rpc_user"]
        self.__rpc_pwd = Settings[currency]["rpc_pwd"]
        self.__user = Settings[currency]["user"]
        self.__access = ServiceProxy("http://%s:%s@%s:%s" % (self.__rpc_user,
                                                             self.__rpc_pwd,
                                                             self.__host,
                                                             self.__port))


    def getbalance(self):
        return self.__access.getbalance()

    def getnewaddress(self):
        return self.__access.getnewaddress(self.__user)

    def listunspent(self):
        return self.__access.listunspent()

    def listtransactions(self):
        if self.__account is None:
            return []
        return self.__access.listtransactions(self.__account, 10000, 0)

    def sendto(self, to_addr, amnt, minconf=3, comment=None):
        if comment is not None:
            return self.__access.sendfrom(self.__user, to_addr, amnt, minconf, comment)
        else:
            return self.__access.sendfrom(self.__user, to_addr, amnt, minconf)
       
              