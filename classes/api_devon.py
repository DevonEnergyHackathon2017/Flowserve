#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$# 

from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
from datetime import datetime
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

class api_devon_osi(object):
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
        list_attributes = ['HHP', 'Treating Pressure', 'Blender Prop Total',
                           'Slurry Total', 'Friction Reducer', 'Gelling Agent', 
                           'Surface Crosslinker', 'Wellname']
#        for string_key in self._attributes:
        for string_key in list_attributes:
            print('getting %s' %string_key)
#            dict_temp[string_key] = self.client.data.get_recorded_values(
#                    self._attributes[string_key], None, None, '10-nov', None, None, 
#                                    100000, None, '18-oct', None)
#            dict_temp[string_key] = self.client.data.get_interpolated_values(
#                    self._attributes[string_key], None, '19-oct-2018 14:00:00', None, 
#                                    None, '00:00:01', None, '19-oct-2018 12:00:00', 
#                                    None)
            dict_temp[string_key] = self.client.data.get_recorded_values(
                    self._attributes[string_key], None, None, '10-nov', None, None, 
                                    100, None, '18-oct', None)
            print('length of %s datraframe: %i' %(string_key, len(dict_temp[string_key])))
            
        min_final, max_final = '', ''
        bool_init = True
        dict_values = dict()
        for string_df in dict_temp:
            if string_df != 'Wellname':
                df_temp = dict_temp[string_df]
                series_time = pandas.to_datetime(df_temp.Timestamp)
                df_temp.index = series_time
                         
                if bool_init == True:
                    min_final = series_time.min()
                    max_final = series_time.max()
                    bool_init = False
                else:
                    if series_time.min() < min_final:
                        min_final = series_time.min()
                    if series_time.max() > max_final:
                        max_final = series_time.max()
                
                series_values = df_temp.Value.copy()
                series_values.index = series_values.index.floor('S')
                series_values_rsmpl = series_values.resample('S').pad()
                series_values_rsmpl.name = string_df
                dict_values[string_df] = pandas.DataFrame(series_values_rsmpl)
            
        print('starting df creation')
        index_df = pandas.date_range(start = min_final, 
                                     end = max_final, freq='S')
        index_df = index_df.floor('S')
        
        df_return = pandas.DataFrame(index = index_df)
        
        for string_key in dict_values:
            df_return = pandas.merge(df_return, dict_values[string_key],
                                     how = 'left', left_index = True, right_index = True)
            
        df_return.fillna(0, inplace = True)
        
        return df_return