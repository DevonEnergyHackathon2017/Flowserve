#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$# 

import json
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
import numpy
import pandas

from warnings import simplefilter
simplefilter('ignore')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Methods
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#

pi_client = PIWebApiClient("https://pi.dvnhackathon.com/piwebapi/", False, 
                           "hacker", "Pa$$w0rd", True) 

df1 = pi_client.data.get_recorded_values(
        "af:\\\\OSISOFTPI-001\\Devon\\Skids\\Skid #77|Active Gel Breaker", 
        None, None, '10-nov', None, None, 100000, None, '18-oct', None)

skid_77 = pi_client.element.get_by_path('\\\\OSISOFTPI-001\\Devon\\Skids\\Skid #77', None)

skid_77.links['Attributes']

#attributes = pi_client.attributes.get_by_path(skid_77.links['Attributes'], None)

attributes = pi_client.element.get_attributes(skid_77.web_id, None, None, None, 
                       None, None, None, None, None, None, None, None, None)