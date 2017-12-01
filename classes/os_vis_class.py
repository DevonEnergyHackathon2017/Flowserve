import numpy as np
import pyodbc
import pandas as pd 
import plotly
import plotly.graph_objs as go

"""
This class will return the FIGURE for a plotly plot of
the old style frac information - NOT the actual plot. 
 
The figure can be plotted with a one liner (commented out at the bottom)
"""
class os_vis(object):
	def __init__(self):
		self.get_data_from_api()
		self.process_data()

		# set chart layout

	def get_data_from_api(self):
		## Rewrite this if you use it - the API call was too slow
		# for our demo
		self._raw_data = pd.read_csv('data/api_sample_data.csv') #directly from API

	def process_data(self):
		self._raw_data = self._raw_data.rename(columns = {'Unnamed: 0':'time_index'})
		self._raw_data.replace([np.inf, -np.inf], np.nan, inplace = True)
		self._raw_data.fillna(0, inplace = True)

	# get figure from imported data
	def blenders(self):
		conc = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Blender Prop Conc'], mode = 'lines', name = 'Concrete Prop')
		calc = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Calc BH Prop Conc'], mode = 'lines', name = 'Calc BH Prop')
		data = [conc, calc]
		fig = go.Figure(data=data)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig

	# slurry plot - these are pretty much all the same
	def slurry(self):
		slurry = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Slurry Rate'], mode = 'lines', name = 'Slurry Rate')
		data = [slurry]
		fig = go.Figure(data=data)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig

	#pressure plot
	def pressure(self):
		pressure = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Treating Pressure'], mode = 'lines', name = 'Treating Pressure')
		data = [pressure]
		fig = go.Figure(data=data)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig

	#concetrations plot
	def concentrations(self):
		friction = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Friction Reducer'], mode = 'lines', name = 'Friction Reducer')
		biocide = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Biocide'], mode = 'lines', name = 'Biocide')
		clay = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Biocide'], mode = 'lines', name = 'Clay Stabilizer')
		surf = go.Scatter(x = self._raw_data['time_index'],
			y = self._raw_data['Biocide'], mode = 'lines', name = 'Surfactant')
		data = [friction, biocide, clay, surf]
		fig = go.Figure(data=data)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig

		# plotly.offline.plot(fig, filename = 'well_model.html')
