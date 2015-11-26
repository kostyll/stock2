import json

def main():
        result = get_trans("watch_result.json")
        events_hash =  {}
        facts = []
        for i in result:
            event = result[i]
            facts.append([i, event['count'], event["prototype"]])
            
        process_facts(facts, result)



def usual_work(fact_res, facts_list, my_res, result, created = {}, deleted={}):
	pass


def tmp_files(fact_res, facts_list, my_res, result, created = {}, deleted={}):
    fact = fact_res[2]
    if fact[2].startswith("/tmp/") and fact[0]=="filesystemevent" :
        if fact_res[0] not in result:
	    return
	del result[fact_res[0]]
	if fact[1] == 'created':
            add_counter(my_res, "tmp_%s_%s" % (fact[1],fact[3]), fact_res[1] )
	    if fact[2] in deleted:
            	add_counter(my_res, "tmp_created_and_deleted", 1 )
		del deleted[fact[2]]
	    else:
		created[fact[2]] = True	
        
	if fact[1] == 'modified':
            add_counter(my_res, "tmp_%s_%s" % (fact[1],fact[3]), fact_res[1] )
  
	if fact[1] == 'deleted':
            add_counter(my_res, "tmp_%s_%s" % (fact[1],fact[3]), fact_res[1] )
	    if fact[2] in created:
            	add_counter(my_res, "tmp_created_and_deleted", 1 )
		del created[fact[2]]
	    else:
		deleted[fact[2]] = True

def uwsgi_tmp_files(fact_res, facts_list, my_res, result):
    fact = fact_res[2]
    if fact[2].startswith("/var/lib/nginx/uwsgi/") and fact[0]=="filesystemevent" :
            del result[fact_res[0]]
            add_counter(my_res, "uwsgi_tmp_%s_%s" % (fact[1],fact[3]), fact_res[1] )
            #print " 1 created and deleted uwsgi temp file %s" % fact[2]

        
def doge_files(fact_res, facts_list, res, result):
     fact = fact_res[2]
     dogecoin = "/data/dogecoin/chainstate/"
     dogecoin2 = "/data/dogecoin/peers"
     dogecoin3 = "/data/dogecoin/wallet.dat"
     dogecoin4 = "/data/dogecoin/blocks"
     dogecoin5 = "/data/dogecoin/logs"
     dogecoin6 = "/data/dogecoin/database"
	
     doge_result_bool = fact[2].startswith(dogecoin6)  or fact[2].startswith(dogecoin5) or fact[2].startswith(dogecoin) or fact[2].startswith(dogecoin2) or fact[2].startswith(dogecoin3)	or fact[2].startswith(dogecoin4)
     if doge_result_bool and fact[0]=="filesystemevent" and fact[1] == 'created':
            del result[fact_res[0]]
            add_counter(res, "dogecoin_create", fact_res[1] )
            return 
     if doge_result_bool and fact[0]=="filesystemevent" and fact[1] == 'deleted':
 
            del result[fact_res[0]]
            add_counter(res, "dogecoin_delete", fact_res[1] )
	    return 
     if doge_result_bool and fact[0]=="filesystemevent" and fact[1] == 'moved':
            del result[fact_res[0]]
            add_counter(res, "dogecoin_moved", fact_res[1] )
	    return
     if doge_result_bool and fact[0]=="filesystemevent" and fact[1] == 'modified':
            del result[fact_res[0]]
            add_counter(res, "dogecoin_modify", fact_res[1] )
	    return
     if fact[2].startswith("/data/dogecoin") and fact[1] == 'modified' and fact[3] == "directory":
            del result[fact_res[0]]
            add_counter(res, "dogecoin_modify", fact_res[1] )
	    return
def mysql_files(fact_res, facts_list, res, result):
     fact = fact_res[2]
     tmp_mysql = "/tmp/MY"
     if fact[2].startswith(tmp_mysql) and fact[0]=="filesystemevent" and fact[1] == 'created':
            del result[fact_res[0]]
            add_counter(res, "mysql_tmp_created", fact_res[1] )
            
     if fact[2].startswith(tmp_mysql) and fact[0]=="filesystemevent" and fact[1] == 'deleted':
 
            del result[fact_res[0]]
            add_counter(res, "mysql_tmp_delete", fact_res[1] )

     if fact[2].startswith(tmp_mysql) and fact[0]=="filesystemevent" and fact[1] == 'modified':
            del result[fact_res[0]]
            add_counter(res, "mysql_tmp_modify", fact_res[1] )

def nginx_http_call_ip(fact_res, facts_list, res, result):
    fact = fact_res[2]
    # url_nginx_call
    if fact[0] == "url_nginx_call_ip":
        add_counter(res, fact_res[0], fact_res[1] )
    	del result[fact_res[0]]        
     
def nginx_http_status(fact_res, facts_list, res, result):
    fact = fact_res[2]
    # url_nginx_call
    if fact[0] == "url_nginx_call_status":
        add_counter(res, fact_res[0], fact_res[1] )
    	del result[fact_res[0]]        
     
def nginx_http_call(fact_res, facts_list, res, result):
    fact = fact_res[2]
    # url_nginx_call
    if fact[0] == "url_nginx_call":
	    for i in  range(1, len(fact)):	
               key = fact[i]
   	       add_counter(res, key, fact_res[1] )
	       for j in  range(i+1, len(fact)):	
		   key = key +","+fact[j]
   	           add_counter(res, key, fact_res[1] )

	    del result[fact_res[0]]        
     
def add_counter(resfacts, facttype, count):
    if facttype in resfacts:
        resfacts[facttype] += int(count)
    else:
        resfacts[facttype] = int(count)
        
        

def process_facts(facts_list, result):
       my_result = {}
       uwsgi_tmp_files_lmb = lambda fact, facts_list, res: uwsgi_tmp_files(fact, facts_list, res, result)
       doge_files_lmb = lambda fact, facts_list, res: doge_files(fact, facts_list, res, result)
       mysql_files_lmb = lambda fact, facts_list, res: mysql_files(fact, facts_list, res, result)
       nginx_http_call_lmb = lambda fact, facts_list, res: nginx_http_call(fact, facts_list, res, result)
       nginx_http_status_lmb = lambda fact, facts_list, res: nginx_http_status(fact, facts_list, res, result)
       nginx_http_call_ip_lmb = lambda fact, facts_list, res: nginx_http_call_ip(fact, facts_list, res, result)
       tmp_files_lmb = lambda fact, facts_list, res: tmp_files(fact, facts_list, res, result)

       
       lambda_funcs =  [nginx_http_call_ip_lmb, nginx_http_call_lmb, nginx_http_status_lmb, 
			uwsgi_tmp_files_lmb, doge_files_lmb, mysql_files_lmb, tmp_files_lmb ]      
       for fact in facts_list:
          for lambda_process in lambda_funcs:
              lambda_process(fact, facts_list, my_result)
       #print my_result
       for i in result:	
       	print i, result[i] 
       
        
        
            
        
            
def get_trans(filename):
    data = None
    with open(filename, 'r') as f:
        data = f.read()
        
    Decoder = json.JSONDecoder()
    Res = Decoder.decode(data)
    return Res



    
main()
