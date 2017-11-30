import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
from well_vis_class import well_vis

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
    html.A(html.Button('Simple View', className='buttons'),
    	href='/simple'),
    html.Br()#,
    #dcc.Link('Detailed View', href = '/page-3')
], style = {'textAlign':'center'})

page_1_layout = html.Div([
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
    html.A(html.Button('Home', className='buttons'),
    	href='./'),

], style = {'textAlign':'center'})

page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.Dropdown(
		id='my-dropdown',
        options=[
            {'label': '2', 'value': 2},
            {'label': '3', 'value': 3}
        ],
        value=2
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    html.A(html.Button('Well Vis', className='buttons'),
    	href='./well_vis'),
    html.Br(),
    html.A(html.Button('Home', className='buttons'),
    	href='./')
])


@app.callback(Output('well_vis', 'figure'), [Input('well_vis_dd', 'value')])
def update_graph(selected_dropdown_value):
    dat = well_vis(selected_dropdown_value)
    return dat.do_plot()

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/well_vis':
        return page_1_layout
    elif pathname == '/simple':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()

