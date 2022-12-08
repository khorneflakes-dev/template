from dash import Dash, html, dcc
import dash
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine


dash.register_page(__name__)

layout = html.Div(children=[
    
    html.Div([
        dcc.Link('Trending', href='/trending'),
        dcc.Link('Risk', href='/risk'),
        dcc.Link('Opportunities', href='/opportunities'),
    ], className='business-menu'),

], className='container')

