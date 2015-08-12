from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from main.models import FullBinInfo
import time
from datetime import timedelta
import json
import urllib2



class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):

            Now = datetime.now()
            L = get_bins()
	    print len(L)
            i=0
	    for item in L:
		Bin = item['bin']
		i+=1
		print i
                try:
                    Bin =  FullBinInfo.objects.get(bin6 = Bin)
                    continue            
                                
                except FullBinInfo.DoesNotExist:
                    pass
                Bin = FullBinInfo(bin6 = item["bin"],
                                      country = item["country"],
                                      product = item["product"],
                                      bank = item["bank"],
                                      prepaid= item["prepaid"],
                                      pbbin = item["pbbin"],
                                      alphacode = item["alphacode"] 
                                      )
                Bin.save()
                
  
def get_bins( ):
    Url = "https://ecommerce.liqpay.com/ecommerce/fullbininfo2"
    
    Decoder = json.JSONDecoder()
    D = urllib2.urlopen(Url)
    Str = D.read()        
    Res = Decoder.decode(Str)
    return Res["fullBinInfoItem"]
