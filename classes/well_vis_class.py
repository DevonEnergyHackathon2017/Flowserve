import numpy as np
import pyodbc
import pandas as pd 
import plotly
import plotly.graph_objs as go

"""
A class to model the 3D orientation of a well bore using deviation survey data.
Since this class is meant to be used in conjunction with a dash application,
the do_plot function returns a figure, the constructor for a plotly graph, but
not the graph itself.

Constructor accepts a wellID to query from sql server.
"""
class well_vis(object):
	def __init__(self, WellId):
		self.WellId = WellId
		self.connection = self.connect_db()

		# getting data
		self._dev_meta_data = self.query_well_deviation_meta('DeviationSurveys')
		self._perf_meta_data = self.query_well_deviation_meta('Perforations')

		# processing and plotting
		self._processed_data = self.process()
		self._plot_data = self.ready_plot_data()

	def connect_db(self):
		conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};' + \
			'PORT=1433;SERVER=dvnhackathondbserver.database.windows.net;' + \
			'DATABASE=CompletionsProblem;UID=SQLREADONLY;PWD=DVNH@ck3r')
		return conn

	def query_well_deviation_meta(self, table):
		query = 'select * from [dbo].' + table + ' where WellId = ' + \
			str(self.WellId)
		return pd.read_sql(query, self.connection)

	# some preprocessing
	def process(self):
		working = pd.concat([
			pd.DataFrame([{'WellId':self.WellId, 'MD':0, 'Incl':0, 'Azm':0}]),
			self._dev_meta_data])
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


	# more preprocessing - before now the meta data is still useful, but now
	# its really just for plotting
	def ready_plot_data(self):
		plot_data = self._processed_data[['cum_disp_dist', 'cum_tvd', 'z_coord']].copy()
		plot_data['cum_tvd'] = plot_data['cum_tvd'] * -1
		plot_data = plot_data[plot_data.apply(lambda x: not any(pd.isnull(x)), axis = 1)]
		plot_data = pd.concat([
			pd.DataFrame([{'cum_disp_dist':0, 'cum_tvd':0, 'z_coord':0}]), plot_data])
		return plot_data

	# creating plotly figure
	def do_plot(self):
		max_lateral_distance = np.max([self._plot_data['z_coord'],
			self._plot_data['cum_disp_dist']])
		true_north_seq = [x for x in range(int(max_lateral_distance))]

		# Assign colors by perforations
		perforation_flag = np.ndarray(shape = (self._processed_data.shape[0],))
		flag = 1
		for x in range(self._processed_data.shape[0]):
			flag = 0
			depth = self._processed_data['MD'][x]
			for y in self._perf_meta_data[['Top', 'Btm']].copy().as_matrix():
				if depth >= y[0] and depth <= y[1]:
					perforation_flag[x] = -1
					flag = 1
					continue
			if flag == 0: perforation_flag[x] = depth

		well_path = go.Scatter3d(
		    x=self._plot_data['cum_disp_dist'],
		    y=self._plot_data['z_coord'],
		    z=self._plot_data['cum_tvd'],
		    marker=dict(
		        color = self._plot_data['cum_tvd'],
		        size=6,
		        symbol='circle',
		        colorscale='Viridis', 
		        line=dict(
		            color='#1f77b4',
		            width=.1
		        ),
		        opacity=.2
		    )
		)

		perforations = go.Scatter3d(
		    x=self._plot_data['cum_disp_dist'].iloc[np.where(perforation_flag == -1)[0]],
		    y=self._plot_data['z_coord'].iloc[np.where(perforation_flag == -1)[0]],
		    z=self._plot_data['cum_tvd'].iloc[np.where(perforation_flag == -1)[0]],
		    mode = 'lines',
		    line=dict(
		        color = '#FF4500',
		        width=6
		    )
		)

		data = [well_path, perforations]

		layout = dict(
		    title='Well Model',
		    showlegend = False,
		    margin=go.Margin(
		        l=50,
		        r=50,
		        b=100,
		        t=100,
		        pad=4
		    ),
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
				    eye=dict(x=3, y=5.5, z=.75)
				)
		    ),
		)

		fig = go.Figure(data=data, layout=layout)
		fig['layout'].update(scene=dict(aspectmode="data"))
		return fig
		# plotly.offline.plot(fig, filename = 'well_model.html')

