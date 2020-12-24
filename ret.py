
#This makes the API call

from google.cloud import datastore
from google.cloud.logging import DESCENDING
import logging
import argparse
import datetime
import rfc3339#, iso8601
from google.cloud import logging
import re
#from google.cloud.logging_v2.handlers import CloudLoggingHandler
def create_header(cf_properties):
    header = list()
    for i in range(0, len(cf_properties)):
        # head = str()
        # for j in range(0, len(cf_properties[i])):
        #     if(j != len(cf_properties[i])-1):
        #         head = head+cf_properties[i][j]+"."
        #     else:
        #         head = head+cf_properties[i][j]
        # header.append(head)
        if(cf_properties[i][-1][0] == ':'):
        	header.append(cf_properties[i][-1][1:])
        else:
            header.append(cf_properties[i][-1])

    return header
def extract(value, attribute_names):
    for attribute_name in attribute_names:
        if(attribute_name[0] != ":"):
            print("getting : ", attribute_name)
            value = getattr(value, attribute_name)

    if(attribute_names[-1][0] == ':'):
        return value[attribute_names[-1][1:]]
    else:
        return value    


def list_entries(logger_name, prjname, cf_list, module_name, sm_name, frequency, cf_properties):
    """Lists the most recent entries for a given logger."""
    
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=-frequency)
    d = d.isoformat("T")+"Z"
    print("=>"+d)
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    print("Listing entries for logger {}:".format(logger.name))
# "logName:"+logger_name+" AND "+
# "resource.type=\"cloud_function\""+" AND "+
    cf_list_str = str()
    cf_dict = dict()

    key_fname = "resource.labels.function_name="
    for i in range(0, len(cf_list)):
        if i != len(cf_list) - 1:
            cf_list_str = cf_list_str + key_fname + "\"" + cf_list[i] + "\"" + " OR "
        else:
            cf_list_str = cf_list_str + key_fname + "\"" + cf_list[i] + "\""
        if cf_list[i] not in cf_dict:
            cf_dict[cf_list[i]] = 0
        # else:
            
    
    FILTER = "resource.type=\"cloud_function\""+" AND "+"resource.labels.project_id="+"\""+prjname+"\""+" AND "+"( "+cf_list_str+") "+" AND "+"receiveTimestamp>="+"\""+d+"\""
#tag module sm function execution started/ended

    notrun = set()
    completed = set()
    running = set()
    # logs = set()


    logs = list(list())
    # //logs.append(cf_properties)
    header = create_header(cf_properties)
    logs.append(header)

    # FILTER = "resource.labels.project_id:"+prjname+" AND "+"resource.labels.function_name:"+cf_name+" AND "+"receiveTimestamp>="+"\""+d+"\""
    
    # FILTER = "resource.labels.function_name:"+cf_name+" AND "+"receiveTimestamp>="+"\""+d+"\""
# , 
# order_by=DESCENDING, 
    # cf_dict = {'retr_log':0, 'delete_fun':1, 'yoyo':1}
    print(FILTER)
    for entry in logger.list_entries(order_by=DESCENDING, filter_=FILTER):
        timestamp = entry.timestamp.isoformat()
        # ---------------------------------------------
        log_record = []
        for i in range(0,len(cf_properties)):
            
            # print("OO : ",cf_properties[i])
            value = extract(entry, cf_properties[i])
            print(" :=> ", value)
            log_record.append(value)
        # print(entry.resource.labels['function_name'])
        # print(getattr(entry, "resource.labels['function_name']"))
        # print("YOY : ", getattr(getattr(entry, 'resource'), 'labels')['function_name'])
        logs.append(log_record)
        # ---------------------------------------------                
        # msg_array = entry.payload.split('|')
        # msg_sm_name = msg_array[2]
        # msg_module_name = msg_array[3]
        # if msg_sm_name != sm_name or msg_module_name != module_name:
        #     continue
        
        print("* {}: {}".format(timestamp, entry))
        print("\n\n")
        # logs.add(str(entry)+"\n")
        isCompleted = bool(re.search(r'Function execution took [0-9]+ ms', entry.payload))
        isStarted = bool(re.search(r'Function execution started', entry.payload))

        if isCompleted and (entry.resource.labels['function_name'] not in running):
            completed.add(entry.resource.labels['function_name'])
        if isStarted and (entry.resource.labels['function_name'] not in completed):
        	running.add(entry.resource.labels['function_name'])
        if (isStarted == False) and (isCompleted == False) and (entry.resource.labels['function_name'] not in completed):
        	running.add(entry.resource.labels['function_name'])



        cf_dict[entry.resource.labels['function_name']] = cf_dict[entry.resource.labels['function_name']] + 1
        print("\n\nRunning : ", entry.resource.labels['function_name'])
    # completed.add('delete_fun')
    # completed.add('retr_log')
    print("cf_dict : ", cf_dict)

    for i in range(0, len(cf_list)):
        if cf_dict[cf_list[i]] == 0:
            notrun.add(cf_list[i])

    # for i in range(0, len(cf_list)):
    #     if(cf_list[i] not in completed) and (cf_list[i] not in notrun):
    #         running.add(cf_list[i])

    print("completed : ", completed)
    print("notrun : ", notrun)    
    print("running : ", running)
    #print("LOGS\n\n\n\n", logs)

    return list(completed), list(notrun), list(running), logs
   


# [END logging_list_log_entries]

#completed, notrun, running, logs = list_entries("cloudfunctions.googleapis.com%2Fcloud-functions", "bda-sandbox", ["delete_fun", "retr_log", "yoyo"], "mod1", "sm1", 180, [("resource","labels", ":function_name"),("severity",), ("timestamp",), ("payload",)])


#rfc3339
#iso8609
#flask
#request
#re
