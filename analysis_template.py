#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#
# File / Package Import
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#  
      
from api_devon_osi.api_devon import api_devon_osi
from collections import Counter
import os
import pandas
import numpy as np
import warnings
import pickle
from datetime import datetime

# supress warnings
warnings.simplefilter('ignore')

api_osi = api_devon_osi()

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

df_skid_77 = api_osi.get_data()
df_skid_77.to_pickle('data/api_call_raw.dat')
with open(r'data/api_call_raw.dat', "rb") as input_file:
 	df_skid_77 = pickle.load(input_file)
#---------------------------------------------------------------------------------------------#
# calculate the costs
#---------------------------------------------------------------------------------------------#

# helper funtion to clear out api failures
def clean_dicts(value_col):
	out = np.array([np.nan if isinstance(x, dict) else x for x in \
		value_col.as_matrix()])
	return out

# helper function to iterate over some similar chemical values
def iter_chems(chem):
	return (clean_dicts(df_skid_77[chem]['Value']) / 60) * (100 / 42)

# get various costs
cost_hhp = np.array(0.25 * df_skid_77['HHP']['Value'] ** 2)
cost_sand = clean_dicts(df_skid_77['Blender Prop Total']['Value']) * .05
cost_water = clean_dicts(df_skid_77['Slurry Total']['Value']) / \
	(clean_dicts(df_skid_77['Blender Prop Total']['Value']) / 928.2) #22.1 * 42

seconds_range = np.array([x for x in range(0, df_skid_77['Blender Prop Total'].shape[0])])
cost_time = [(10000 / 3600)] * len(cost_hhp)
          
cost_frict_red = iter_chems('Friction Reducer')
cost_gell_ag = iter_chems('Gelling Agent')
cost_sur_cross = iter_chems('Surface Crosslinker')

cost_total = cost_hhp + cost_sand + cost_water + cost_frict_red + cost_gell_ag + \
	cost_sur_cross + cost_time

output_df = pandas.DataFrame({
	'cost_time':cost_time,
	'cost_sur_cross':cost_sur_cross,
	'cost_hhp':cost_hhp,
	'cost_sand':cost_sand,
	'cost_water':cost_water,
	'cost_frict_red':cost_frict_red,
	'cost_gell_ag':cost_gell_ag,
	'cost_total':cost_total,
})
output_df.to_csv('data/api_cost_sample_data.csv')

# get value columns from all attributes
value_list = []
col_names = []
for x in df_skid_77.iteritems():
	col_names.append(x[0])
	df_extract = clean_dicts(x[1]['Value'])
	value_list.append(df_extract)
output_vals = pandas.DataFrame(value_list)
output_vals = output_vals.transpose()
output_vals.columns = col_names
output_vals.to_csv('data/api_sample_data.csv')

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