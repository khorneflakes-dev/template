import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    
    html.Img(src='./assets/logo.png', className='mainlogo'),
    html.P('PLUS YELP', className='title'),
    
        
], className='home')