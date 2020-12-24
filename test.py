
#This hosts the server
from flask import Flask, request, render_template
import ret
import json
app = Flask(__name__)

import configparser
import gcsfs

configparser = configparser.ConfigParser()
filename = 'config.ini'
configparser.read(filename)

reg_list = configparser.sections()

prjname = "NULL"
cf_list = []
module_list = []
sm_list = []
frequency = 90 #90 seconds by default

config = dict()
config['reg_list'] = list()
for registry in configparser.sections():
	prjname = configparser.get(registry, 'prjname')
	module_list = configparser.get(registry, 'ModuleName').split(',')
	sm_list = configparser.get(registry, 'SMName').split(',')
	cf_list = configparser.get(registry, 'CFname').split(',')
	frequency = configparser.getint(registry, 'frequency')
	properties = configparser.get(registry, 'properties').split(',')
	
	properties_ = list(list())

	for prop in properties:
		cur = prop.split('.')
		if(cur[-1] in ("function_name" , "project_id", "region")):
			cur[-1] = ":"+cur[-1]
		properties_.append(cur)
	print("PROP : ",properties_)	

	config[registry] = json.dumps({
		'prjname' : prjname,
		'module_list' : module_list,
		'sm_list' : sm_list,
		'cf_list' : cf_list,
		'frequency' : frequency,
		'properties' : properties_
	})
	# config[registry] = json.dumps({
	# 	'prjname' : json.dumps(prjname),
	# 	'module_list' : json.dumps(module_list),
	# 	'sm_list' : json.dumps(sm_list),
	# 	'cf_list' : json.dumps(cf_list),
	# 	'frequency' : json.dumps(frequency),
	# 	'properties' : json.dumps(properties)
	# })
	# print("PROP : ", config['bda']['properties'])
	# print("TYPETYPE : ", type(config['bda']))
	config['reg_list'].append(registry)


def sort_ascending(logs):
	for i in range(1, (len(logs)-1)//2+1):
		logs[i], logs[len(logs) - i] = logs[len(logs) - i], logs[i]

@app.route('/extract_logs/<module_name>/<sm_name>/<current_registry>/<current_autorefresh>')
def extract_logs(module_name, sm_name, current_registry, current_autorefresh):
	print("Extracting Logs.......\n")
	# completed_cfs = ['cc1', 'cc2', 'cc3']
	# running_cfs = ['retr_log', 'rc2', 'rc3']
	# notrun_cfs = ['delete_fun', 'nr2', 'nr3']
	# logs = [["H1","H2","H3"],["R11", "R12","R13"],["R21","R22","R23"],["R31","R32","R33"]]
	# print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
	
	
	# print(logs)
	conf = json.loads(config[current_registry])
	cf_properties = conf['properties']
	# completed_cfs, notrun_cfs, running_cfs, logs = ret.list_entries("cloudfunctions.googleapis.com%2Fcloud-functions", prjname, cf_list, module_name, sm_name, frequency, cf_properties)
	sort_ascending(logs)
	print(logs)
	return {"completed_cfs":completed_cfs, "notrun_cfs":notrun_cfs, "running_cfs":running_cfs, "logs":logs}
	# return render_template("index.html", completed_cfs, running_cfs, logs, frequency)
	# return "None"
	


@app.route('/')
def index():
	# print("Running /")
	return render_template("index.html", config=config)



if __name__ == "__main__":
	app.run(host='127.0.0.9',port=4465,debug=True)
	# app.run(debug=True)


# @app.route('/CFlogs/<cfname>')
# def getCFLogs():
# 	return "HELLO"
