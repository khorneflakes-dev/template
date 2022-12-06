from dash import Dash, dcc, html, Input, Output, State, ctx
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import math

# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')

app = Dash(__name__)
app.config.suppress_callback_exceptions=True

app.title = 'YELP'
server = app.server



app.layout = html.Div([
     
    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),

    # business-container 1
    html.Div([
        
        html.Div([
            html.Div([
                
                html.P('filter by:'),
                
                dcc.Dropdown(['Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants'], 'Restaurants', id='categories'),
                
                dcc.RangeSlider(2005, 2021, 1, value=[2017, 2021], id='year-slider')
                
            ],className='row1-col1-row1'), # filter y slider
            
            html.Div([
                
                html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.'),
                
                html.Div([
                    
                    html.P('CUSTOMER EXPERIENCE SATISFACTION (Percentage of reviews with stars>=4)'),
                    
                    dcc.Graph(id='experience-map')
                                        
                ], className='experience-container')
                                
            ], className='row1-col1-row2')
                        
        ], className='row1-col1'), # primer col + descripcion
        
        html.Div([
            
            html.P('Data Driven Investing Dashboard'),
            
            html.Div([
                
                html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.'),
                
                html.Div([
                    
                    dcc.Graph(id='heatmap-trends')
                    
                ], className='heatmap-tendencias')
                
            ], className='row1-col2-col2')
            
        ], className='row1-col2'),
        
    ], className='business-row1'), #primera fila de business1
    
    html.Div([
        
        html.Div([
            
            html.P('TOP 10 BUSINESS BY CUSTOMER RETENTION'),
            
            dcc.Graph(id='top-retention')
            
        ], className='row1-col1'),
        
        
        html.Div([
                        
            html.P('TOP 10 BUSINESS BY CUSTOMER SATISFACTION'),
            
            dcc.Graph(id='top-satisfaction')
            
        ], className='row1-col2'),
        
        
        html.Div([
        
            dcc.RadioItems(['Categories', 'Attributes'], 'Categories'),
            
            dcc.Graph(id='wordcloud'),
            
            html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.')
            
        ], className='row1-col3'),
      
    ], className='business-row2'),
     
], className = 'business1-container')



if __name__ == '__main__':
    app.run_server(debug=True)
