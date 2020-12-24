from google.cloud import datastore
from google.cloud.logging import DESCENDING
import logging
import argparse
import datetime
import rfc3339#, iso8601
from google.cloud import logging



# This is a temporary file which has been used for testing purpose


def create_header(cf_properties):
    header = list()
    for i in range(0, len(cf_properties)):
        head = str()
        for j in range(0, len(cf_properties[i])):
            if(j != len(cf_properties[i])-1):
                head = head+cf_properties[i][j]+"."
            else:
                head = head+cf_properties[i][j]
        header.append(head)
    return header

"""Lists the most recent entries for a given logger."""
def extract(value, attribute_names):
    for attribute_name in attribute_names:
        if(attribute_name[0] != ":"):
            print("getting : ", attribute_name)
            value = getattr(value, attribute_name)

    if(attribute_names[-1][0] == ':'):
        return value[attribute_names[-1][1:]]
    else:
        return value
def list_entries(logger_name, prjname, cf_name, frequency, cf_properties):

    curtime = datetime.datetime.utcnow()
    prevtime = curtime + datetime.timedelta(seconds=-frequency)
    prevtime = prevtime.isoformat("T")+"Z"

    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    print("Listing entries for logger {}:".format(logger.name))    

    
    curtime = curtime.isoformat("T")+"Z"
    
    FILTER = "resource.type=\"cloud_function\""+" AND "+"resource.labels.project_id="+"\""+prjname+"\""+" AND "+ "resource.labels.function_name="+cf_name+" AND "+"receiveTimestamp>="+"\""+prevtime+"\""
    #+" AND "+"receiveTimestamp<="+"\""+curtime+"\""

    logs = list(list())
    # logs.append(cf_properties)
    header = create_header(cf_properties)
    logs.append(header)


    for entry in logger.list_entries(order_by=DESCENDING, filter_=FILTER):
        # if(entry.timestamp < prevtime or entry.timestamp > curtime):
        #     print("nope")
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
        timestamp = entry.timestamp.isoformat()
        print("* {}: {}".format(timestamp, entry.payload))
        print("TYPE : ",type(entry), "\n")
    # print(extract("value"))
    print("logs : ", logs)
list_entries("cloudfunctions.googleapis.com%2Fcloud-functions", "bda-sandbox", "delete_fun", 190, [["resource","labels", ":function_name"],["severity"], ["timestamp"], ["payload"]])