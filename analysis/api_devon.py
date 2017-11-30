#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$# 

from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
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

class api_devon_osi():
    def __init__(self):
        self.client = PIWebApiClient("https://pi.dvnhackathon.com/piwebapi/", False, 
                               "hacker", "Pa$$w0rd", True) 
        self._base_path = '\\\\OSISOFTPI-001\\Devon\\Skids\\Skid #77'
        self._skid_77 = self.client.element.get_by_path(self._base_path, None)
        self._attributes = self._get_attributes(self._skid_77)

    def _get_attributes(self, m_skid_77):
        dict_temp = dict()
        attributes = self.client.element.get_attributes(m_skid_77.web_id, None, None, None, 
                       None, None, None, None, None, None, None, None, None)
        for item in attributes.items:
            dict_temp[item.name] = 'af:' + item.path
        return dict_temp

    def get_data(self):
        dict_temp = dict()
        for string_key in self._attributes:
            dict_temp[string_key] = self.client.data.get_recorded_values(self._attributes[string_key], None, None, '10-nov', None, None, 100000, None, '18-oct', None)
        return pandas.Panel(dict_temp)