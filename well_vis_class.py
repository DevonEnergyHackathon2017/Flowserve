import math
import numpy as np
import pyodbc
import pandas as pd 
import plotly
import plotly.graph_objs as go

class well_vis(object):
	def __init__(self, WellId):
		self.WellId = WellId
		self.connection = self.connect_db()
		self._meta_data = self.query_well_deviation_meta()
		self._processed_data = self.process()
		self._plot_data = self.ready_plot_data()

	def connect_db(self):
		conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};' + \
			'PORT=1433;SERVER=dvnhackathondbserver.database.windows.net;' + \
			'DATABASE=CompletionsProblem;UID=SQLREADONLY;PWD=DVNH@ck3r')
		return conn

	def query_well_deviation_meta(self):
		query = 'select * from [dbo].[DeviationSurveys] where WellId = ' + \
			str(self.WellId)
		return pd.read_sql(query, self.connection)

	def process(self):
		working = pd.concat([
			pd.DataFrame([{'WellId':self.WellId, 'MD':0, 'Incl':0, 'Azm':0}]),
			self._meta_data])
		working.reset_index(inplace = True, drop = True)
		lookahead_length = np.array((working['MD'] - working['MD'].shift(1))[1:])
		lookahead_length = np.append(lookahead_length, None)
		working['lookahead_length'] = lookahead_length

				# get change in depths and displacement from 0
		working['delta_disp_dist'] = working['lookahead_length'] * \
			np.sin(working['Incl'] * 0.0174532925)
		working['delta_tvd'] = working['lookahead_length'] * \
			np.cos(working['Incl'] * 0.0174532925)

		# get cum sums
		working['cum_disp_dist'] = working['delta_disp_dist'].cumsum()
		working['cum_tvd'] = working['delta_tvd'].cumsum()

		# get orientation from true north
		working['z_coord'] = working['cum_disp_dist'] * \
			np.cos(working['Azm'] * 0.0174532925)
		working['z_coord'] = working['z_coord'] - working['z_coord'] * np.sin(45)

		return working

	def ready_plot_data(self):
		plot_data = self._processed_data[['cum_disp_dist', 'cum_tvd', 'z_coord']].copy()
		plot_data['cum_tvd'] = plot_data['cum_tvd'] * -1
		plot_data = plot_data[plot_data.apply(lambda x: not any(pd.isnull(x)), axis = 1)]
		plot_data = pd.concat([
			pd.DataFrame([{'cum_disp_dist':0, 'cum_tvd':0, 'z_coord':0}]), plot_data])
		return plot_data

	def do_plot(self):
		max_lateral_distance = np.max([self._plot_data['z_coord'],
			self._plot_data['cum_disp_dist']])
		true_north_seq = [x for x in range(int(max_lateral_distance))]

		trace = go.Scatter3d(
		    x=self._plot_data['cum_disp_dist'],
		    y=self._plot_data['z_coord'],
		    z=self._plot_data['cum_tvd'],
		    marker=dict(
		        color=self._plot_data['cum_tvd'],
		        size=4,
		        symbol='circle',
		        colorscale='Viridis', 
		        line=dict(
		            color='#1f77b4',
		            width=.33
		        ),
		        opacity=.7
		    )
		)

		data = [trace]

		layout = dict(
		    width= 1150,
		    height=800,
		    autosize=False,
		    title='Well Model',
		    showlegend = False,
		    scene=dict(
		        xaxis=dict(
		        	title = 'Distance',
		            gridcolor='rgb(255, 255, 255)',
		            zerolinecolor='rgb(255, 255, 255)',
		            showbackground=True,
		            backgroundcolor='rgb(230, 230,230)'
		        ),
		        yaxis=dict(
		        	title = '',
		            gridcolor='rgb(255, 255, 255)',
		            zerolinecolor='rgb(255, 255, 255)',
		            showbackground=True,
		            backgroundcolor='rgb(230, 230,230)',
		            autorange=True,
			        showgrid=False,
			        zeroline=False,
			        showline=False,
			        ticks='',
			        showticklabels=False
		        ),
		        zaxis=dict(
		        	title = 'Depth',
		            gridcolor='rgb(255, 255, 255)',
		            zerolinecolor='rgb(255, 255, 255)',
		            showbackground=True,
		            backgroundcolor='rgb(230, 230,230)'
		        ),

		        camera = dict(
				    up=dict(x=1, y=1, z=1),
				    center=dict(x=0, y=0, z=0),
				    eye=dict(x=1.5, y=3.75, z=.5)
				)
		    ),
		)

		fig = go.Figure(data=data, layout=layout)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig
		# plotly.offline.plot(fig, filename = 'well_model.html')