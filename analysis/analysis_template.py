#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#  
      
from api_devon import api_devon_osi
from Timer import Timer
from collections import Counter
import os
import pandas
import numpy
import warnings

# supress warnings
warnings.simplefilter('ignore')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Main Method
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#


'''
this is the main method tests the bulk insert and single insert for the SqlInsertIntoTable method
 
Requirements:
None

Inputs:
list_args
Type: list
Desc: arguements for login to the sql server
list_args[0] -> type: string; user name
list_args[1] -> type: string; password
      
Important Info:
None

Return:
None
Type: None
Description: None
'''

#---------------------------------------------------------------------------------------------#
# object declarations
#---------------------------------------------------------------------------------------------#

api_osi = api_devon_osi()

#---------------------------------------------------------------------------------------------#
# time declarations
#---------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------#
# iteration declarations (list, set, tuple, counter, dictionary)
#---------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------#
# variables declarations
#---------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------#
# db connections
#---------------------------------------------------------------------------------------------#

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# Start
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

#---------------------------------------------------------------------------------------------#
# pull the data from the osi api
#---------------------------------------------------------------------------------------------#

timer_pull_data = Timer()
df_skid_77 = api_osi.get_data()
timer_pull_data.stop_timer('time to pull all the data:')
del timer_pull_data

#---------------------------------------------------------------------------------------------#
# calculate the costs
#---------------------------------------------------------------------------------------------#

df_skid_77['cost_hhp'] = 0.25 * df_skid_77['HHP'] ** 2
df_skid_77['cost_sand'] = df_skid_77['Blender Prop Total'] * 0.05
df_skid_77['cost_water'] = df_skid_77['Slurry Total'] - \
          (df_skid_77['Blender Prop Total'] / (22.1 * 42))
          
dict_chem = {'fr':['Friction Reducer','cost_frict_red'], 'ga':['Gelling Agent', 'cost_gell_ag'], 
             'sc':['Surface Crosslinker', 'cost_sur_cross']}
for string_chem in dict_chem:
    df_skid_77[dict_chem[string_chem][1]] = (df_skid_77[dict_chem[string_chem][0]] / 60) * \
              (100 / 42)
    df_skid_77[dict_chem[string_chem][1]] = df_skid_77[dict_chem[string_chem][1]].cumsum()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# sectional comment
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#                

#---------------------------------------------------------------------------------------------#
# variable / object cleanup
#---------------------------------------------------------------------------------------------#