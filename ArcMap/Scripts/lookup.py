#! /usr/bin/env python3

# Note: https URLs possibly cause Geoprocessing scripts to hang...

import json
import arcpy


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# Parameter passed from Arc tool
in_workspace = arcpy.GetParameterAsText(0)

# Macrostrat URL (with appended parameter from user)
url = 'http://macrostrat.org/api/v2/defs/strat_names?strat_name_like=' + in_workspace

arcpy.AddMessage('before hitting API url')
arcpy.AddMessage(url)

# Retrieve JSON
response = urlopen(url).read().decode()
response_as_json = json.loads(response)

# Send back response as JSON
# TODO improve flexibility of call, possibly remove hard-coded indent level
arcpy.AddMessage(json.dumps(response_as_json, indent=4))

