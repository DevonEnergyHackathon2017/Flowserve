import dash
import pandas as pd
import numpy as np
import datetime as dt
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
from classes.well_vis_class import well_vis
from classes.os_vis_class import os_vis

# helper function to color the JPI cards in the dashboard view
# have to hook this up to the real time streamer later..
def kpi_indexer(kpi):
    time_now = dt.now()
    sec = time_now.second
    minute = time_now.minute
    hour = time_now.hour

    # using the time now as row index - we can use this with the timestamp 
    # later
    row = int(((hour * 3600) + (minute * 60) + (sec)))
    if kpi == 1:
        out = _cost_data['cum_total_cost'][row]
    elif kpi == 2:
        out = _cost_data['cum_cost_sand_water'][row]
    elif kpi == 3:
        out = _raw_data['Treating Pressure'][row]
    elif kpi == 4:
        out = _raw_data['Slurry Rate'][row]
    return out

# second helper function for KPI streaming demo
# just switches the color values based on cutoffs and which KPI
# - not as complicated as it looks
# returns an html button obj
def kpi_colorizer(kpi):
    last_value = kpi_indexer(kpi)

    if kpi == 1:
        kpi_name = 'Cumulative Total Cost: '
        if last_value > 100000:
            col = 'rgb(255, 0, 0)'
        elif last_value > 50000:
            adjust = (last_value / 100000) * 255
            col = 'rgb(255,' + str(int(adjust)) + ', 0)'
        else:
            adjust = (last_value / 50000) * 255
            col = 'rgb(' + str(int(adjust)) + ', 255, 0)'
    elif kpi == 2:
        kpi_name = 'Cumulative Sand + Water Cost: '
        if last_value > 40000:
            col = 'rgb(255, 0, 0)'
        elif last_value > 20000:
            adjust = (last_value / 40000) * 255
            col = 'rgb(255,' + str(int(adjust)) + ', 0)'
        else:
            adjust = (last_value / 20000) * 255
            col = 'rgb(' + str(int(adjust)) + ', 255, 0)'
    elif kpi == 3:
        kpi_name = 'Treating Pressure: '
        if last_value > 8000:
            col = 'rgb(255, 0, 0)'
        elif last_value > 5000:
            adjust = (last_value / 8000) * 255
            col = 'rgb(255,' + str(int(adjust)) + ', 0)'
        else:
            adjust = (last_value / 5000) * 255
            col = 'rgb(' + str(int(adjust)) + ', 255, 0)'
    elif kpi == 4:
        kpi_name = 'Slurry Rate: '
        if last_value > 50:
            col = 'rgb(0, 255, 0)'
        elif last_value > 35:
            adjust = (1 - (last_value / 50)) * 255
            col = 'rgb(' + str(int(adjust)) + ', 255, 0)'
        else:
            adjust = (1 - (last_value / 35)) * 255
            col = 'rgb(255,' + str(int(adjust)) + ', 0)'
    out_string = '${:,.2f}'.format(last_value) if kpi in [1,2] else last_value
    out = html.Div(html.A(html.Button(kpi_name + str(out_string),
                        style = {'background-color': col,
                                 'height':'250',
                                 'width':'50%',
                                 'float':'left',
                                 'font-size':20,
                                 'color':'black'})))
    return out

# Init app
app = dash.Dash('Well Completions Optimizer')
app.config.suppress_callback_exceptions = True

# do some data prep for kpi dashboarding
_raw_data =pd.read_csv('C:/Users/10154928/Flowserve/data/api_sample_data.csv')
_cost_data =  pd.read_csv('C:/Users/10154928/Flowserve/data/api_cost_sample_data.csv')
#process
_raw_data = _raw_data.rename(columns = {'Unnamed: 0':'time_index'})
_cost_data = _cost_data.rename(columns = {'Unnamed: 0':'time_index'})

_raw_data.replace([np.inf, -np.inf], np.nan, inplace = True)
_cost_data.replace([np.inf, -np.inf], np.nan, inplace = True)
_raw_data.fillna(0, inplace = True)
_cost_data.fillna(0, inplace = True)

_cost_data['cum_total_cost'] = _cost_data['cost_total'].cumsum()
_cost_data['cum_cost_sand_water'] = _cost_data['cost_sand'].cumsum() + \
    _cost_data['cost_water']

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
	html.H1('Well Completions Tool'),
	html.Br(),
	html.Br(),
    html.Div([
        html.A(html.Button('Home', className='buttons'),
            href='./', style = {'width':'33%'}),
        html.A(html.Button('Well Visualization', className='buttons'),
            href='./well_vis', style = {'width':'33%'}),
        html.A(html.Button('Dashboard', className='buttons'),
            href='./simple', style = {'width':'33%'}),
        html.A(html.Button('Retro View', className='buttons'),
            href='./retro', style = {'width':'33%'})
    ])
], style = {'textAlign':'center'})

well_vis_layout = html.Div([
    html.H1('Wellbore Visualization'),
    html.H3('Based on Deviation Survey'),
    html.Div(
        dcc.Dropdown(
    		id='well_vis_dd',
            options=[
                {'label': 'Well Id 1', 'value': 1},
                {'label': 'Well Id 2', 'value': 2},
                {'label': 'Well Id 3', 'value':3}
            ],
            value=1
        ), style = {'width':'100%', 'textAlign':'center'}
    ),
   	dcc.Graph(id='well_vis', style={'height': '700px'}), 
    html.Div([
        html.A(html.Button('Home', className='buttons'),
            href='./', style = {'width':'33%'}),
        html.A(html.Button('Dashboard', className='buttons'),
            href='./simple', style = {'width':'33%'}),
        html.A(html.Button('Retro View', className='buttons'),
            href='./retro', style = {'width':'33%'})
    ])

], style = {'textAlign':'center'})

simple_layout = html.Div([
    html.H5('Well KPI Dashboard'),
    html.Br(),
 # contains the kpi buttons - they dont have any function
    html.Div([
        html.Div(id = 'KPI1'),
        html.Div(id = 'KPI2'),
        html.Div(id = 'KPI3'),
        html.Div(id = 'KPI4'),
        dcc.Interval(id='kpiupdate', interval=1000),
    ], style = {'textAlign':'center'}),
    html.Div([
        html.A(html.Button('Home', className='buttons'),
            href='./', style = {'width':'33%'}),
        html.A(html.Button('Well Visualization', className='buttons'),
            href='./well_vis', style = {'width':'33%'}),
        html.A(html.Button('Retro View', className='buttons'),
            href='./retro', style = {'width':'33%'})
    ])
], style = {'textAlign':'center'})


# layout for the retro style
retro_layout = html.Div([
    html.H1('Retro Style Frac Data Display'),

    html.Div(
        dcc.Dropdown(
            id='retro_vis_dd',
            options=[
                {'label': 'Treating Pressure', 'value': 'pressure'},
                {'label': 'Slurry Rate', 'value': 'slurry'},
                {'label': 'Concentrations', 'value':'concen'},
                {'label': 'Blender Prop Conc', 'value':'blend'}
            ],
            value=1
        ), style = {'width':'100%', 'textAlign':'center'}
    ),
    html.Div([
        dcc.Graph(id='retro_chart')
    ]),

    html.Div([
        html.A(html.Button('Home', className='buttons'),
            href='./', style = {'width':'33%'}),
        html.A(html.Button('Well Visualization', className='buttons'),
            href='./well_vis', style = {'width':'33%'}),
        html.A(html.Button('Dashboard View', className='buttons'),
            href='./simple', style = {'width':'33%'})
    ])

], style = {'textAlign':'center'})
    
# Callback to update the well 3d vis
@app.callback(Output('retro_chart', 'figure'), [Input('retro_vis_dd', 'value')])
def update_graph(selected_dropdown_value):
    retro_vis = os_vis()
    if selected_dropdown_value == 'slurry':
        fig = retro_vis.slurry()
    elif selected_dropdown_value == 'concen':
        fig = retro_vis.concentrations()
    elif selected_dropdown_value == 'blend':
        fig = retro_vis.blenders()
    elif selected_dropdown_value == 'pressure':
        fig = retro_vis.pressure()

    return fig

# Callback to update the well 3d vis
@app.callback(Output('well_vis', 'figure'), [Input('well_vis_dd', 'value')])
def update_graph(selected_dropdown_value):
    dat = well_vis(selected_dropdown_value)
    return dat.do_plot()

# Updating all 4 KPIs
##########
@app.callback(Output('KPI1', 'children'), [], [],
    [Event('kpiupdate', 'interval')])
def update_kpi_buttons():
    return kpi_colorizer(1)

@app.callback(Output('KPI2', 'children'), [], [],
    [Event('kpiupdate', 'interval')])
def update_kpi_buttons():
    return kpi_colorizer(2)

@app.callback(Output('KPI3', 'children'), [], [],
    [Event('kpiupdate', 'interval')])
def update_kpi_buttons():
    return kpi_colorizer(3)

@app.callback(Output('KPI4', 'children'), [], [],
    [Event('kpiupdate', 'interval')])
def update_kpi_buttons():
    return kpi_colorizer(4)

#############

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/well_vis':
        return well_vis_layout
    elif pathname == '/simple':
        return simple_layout
    elif pathname == '/retro':
        return retro_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()
