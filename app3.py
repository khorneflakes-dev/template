from dash import Dash, html, dcc
import dash
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine 

# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')

# external JavaScript files
external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']

# external CSS stylesheets
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']

app = Dash(__name__, use_pages=True,
           external_scripts=external_scripts,
           external_stylesheets=external_stylesheets)

# server = app.server
app.layout = html.Div([
    html.Nav([
        html.Div([
            html.A('Logo', className='brand-logo right', href='#!'),
            # html.A([html.I('menu', className='material-icons')], **{'data-target': 'mobile-demo'},className='sidenav-trigger', href='#' ),
            html.Ul([
                html.Li([dcc.Link('home', href='/'),]),
                html.Li([dcc.Link('analytics', href='/analytics'),]),
                html.Li([dcc.Link('users', href='/users'),]),
                html.Li([dcc.Link('about us', href='/about'),]),
            ], className='hide-on-med-and-down center navbar-left'),
        ], className='nav-wrapper navbar'),
    ]),
    
    
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)