#! /usr/bin/env python3

# Note: https URLs possibly cause Geoprocessing scripts to hang...

import urllib.request
import json
import arcpy

# Parameter passed from Arc tool
in_workspace = arcpy.GetParameterAsText(0)

# Macrostrat URL (with appended parameter from user)
url = 'http://macrostrat.org/api/v2/defs/strat_names?strat_name_like=' + in_workspace

arcpy.AddMessage('before hitting API url')
arcpy.AddMessage(url)

# Retrieve JSON
response = urllib.request.urlopen(url).read().decode()
response_as_json = json.loads(response)

# Send back response as JSON
# TODO improve flexibility of call, possibly remove hard-coded indent level
arcpy.AddMessage(json.dumps(response_as_json, indent=4))














#parsing response
# r = urllib.request.urlopen(req).read()
# print(r)
# cont = json.loads(r.decode('utf-8'))
# counter = 0
#
# ##parcing json
# for item in cont['data']['children']:
#     counter += 1
#     print("strat_name:", item['data']['strat_name'], "strat_name_long:", item['data']['strat_name_long'])
#     print("----")
#
# ##print formated
# #print (json.dumps(cont, indent=4, sort_keys=True))
# print("Number of names: ", counter)
