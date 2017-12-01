import dash
import numpy as np
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
from classes.well_vis_class import well_vis

#helper functions
def kpi_colorizer(kpi):
    val = 100
    if kpi == 1:
        val = np.random.random() * val * 2
        if val > 150:
            col = '#ff0000'
        elif val > 100:
            col = '#EEE8AA'
        else: 
            col = '#4CAF50'
    elif kpi == 2:
        col = '#ff0000'
    else:
        col = '#ff2200'
    return col

# Init app
app = dash.Dash('Well Completions Optimizer')
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
	html.H1('Well Completions Tool'),
	html.Br(),
	html.Br(),
	html.Br(),
	html.A(html.Button('Well Visualization', className='buttons'),
    	href='/well_vis'),
    html.Br(),
    html.Br(),
    html.A(html.Button('Simple View', className='buttons'),
    	href='/simple'),
    html.Br()#,
    #dcc.Link('Detailed View', href = '/page-3')
], style = {'textAlign':'center'})

well_vis_layout = html.Div([
    html.H1('Well Visualization'),
    html.H3('Based on Deviation Survey'),
    dcc.Dropdown(
		id='well_vis_dd',
        options=[
            {'label': 'Well Id 1', 'value': 1},
            {'label': 'Well Id 2', 'value': 2},
            {'label': 'Well Id 3', 'value':3}
        ],
        value=1
    ),
   	dcc.Graph(id='well_vis', style={'height': '700px'}),
    # html.Div(id='page-1-content'),
    html.Br(),
    html.A(html.Button('Simple View', className='buttons'),
    	href='./simple'),
    html.Br(),
    html.Br(),
    html.A(html.Button('Home', className='buttons'),
    	href='./'),

], style = {'textAlign':'center'})

simple_layout = html.Div([
    html.H5('Well KPI Dashboard'),
    html.Br(),

    # contains the kpi buttons - they dont have any function
    html.Div([
        html.Div([
                html.Div(html.A(html.Button('KPI #1',
                    style = {'background-color': '#4CAF50',
                             'height':'250',
                             'width':'50%',
                             'float':'left'}))),
        ]),
        html.Div([
                html.Div(html.A(html.Button('KPI #2', id = 'kpi1button',
                    style = {'background-color': kpi_colorizer(1),
                             'height':'250',
                             'width':'50%',
                             'float':'left'}))),
        ]),
        html.Div([
                html.Div(html.A(html.Button('KPI #3',
                    style = {'background-color': kpi_colorizer(1),
                             'height':'250',
                             'width':'50%',
                             'float':'left'}))),
        ]),
        html.Div([
                html.Div(html.A(html.Button('KPI #4',
                    style = {'background-color': kpi_colorizer(2),
                             'height':'250',
                             'width':'50%',
                             'float':'left'}))),
        ]),
        dcc.Interval(id='kpiupdate', interval=1000),
    ], style = {'textAlign':'center'}),
    html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.A(html.Button('Well Visualization', className='buttons'),
            href='./well_vis', style = {'width':'50%'}),
        html.A(html.Button('Home', className='buttons'),
            href='./', style = {'width':'50%'})
    ])
], style = {'textAlign':'center'})


@app.callback(Output('well_vis', 'figure'), [Input('well_vis_dd', 'value')])
def update_graph(selected_dropdown_value):
    dat = well_vis(selected_dropdown_value)
    return dat.do_plot()

@app.callback(Output('kpi1button', 'figure'), [], [],
    [Event('kpiupdate', 'interval')])
def update_kpi_buttons():
    return kpi_colorizer(1)

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/well_vis':
        return well_vis_layout
    elif pathname == '/simple':
        return simple_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()

