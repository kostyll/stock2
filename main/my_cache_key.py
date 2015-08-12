import hashlib
import base64
from lockfile import FileLock, LockTimeout
from django.core.cache import get_cache
import calendar
from time import gmtime
from crypton import settings


def caching():
      return  get_cache('default')

def check_freq(Type, Count):
	Now = calendar.timegm(gmtime())
	cache = caching()
        Prev = cache.get(Type)
	if Prev :
		Prev = int(Prev)
		if Now - Prev > Count:
			cache.set(Type, str(Now))
			return True
	else:
		cache.set(Type, str(Now))
		return True

	return False
def make_cached_key(key, key_prefix, version):
    Md5 =  hashlib.md5(key_prefix + str(key))    
    return    base64.b64encode( Md5.digest() )


def my_lock(LockFile, TimeOut = 3):
        lock = FileLock(settings.ROOT_PATH + LockFile)
        IsLock = False
        try:
                lock.acquire(timeout = TimeOut)    # wait up to 60 seconds
                IsLock = True
        except LockTimeout:
                IsLock = False
        
        if IsLock :
                return lock
        else:
                raise LockBusyException("Lock is busy")
        
class LockBusyException(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)       
 
 
def my_release(lock): 
        if lock is None :
               return False
        lock.release()
        return True
