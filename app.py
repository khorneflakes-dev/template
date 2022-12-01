from dash import Dash, dcc, html, Input, Output, State
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine


# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')


app = Dash(__name__)


app.title = 'YELP'
server = app.server



app.layout = html.Div([
    
    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),
    
    
    html.Div([
        
        html.Div([
            
            dcc.Textarea(id='textarea2', className='user', placeholder='enter id user'),
            
            html.Button('login', id='textarea-state-example-button', n_clicks=0, className='login'),
            
        ], className='login-area'),
        
        html.Div(id='day', className='day')
        
    ], className='row1-1'),
        
    html.Div([
        html.Div('Welcome',id='textarea-state-example-output', className=''),
    ], className='row1-2')
       
    
], className = 'main-container')



# funcion para validar el id_user
@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea2', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0 and value != None:
        return f'Welcome, {value}'
    else:
        return 'Welcome'



# funcion para retornar el dia y la hora para la ciudad de argentina
@app.callback(
    Output('day', 'children'),
    [Input('aux', 'value')]
)
def actual_day(value):
    from datetime import datetime
    import pytz
    dt = datetime.now(pytz.timezone('America/Buenos_Aires'))
    return '{}, {}'.format(dt.strftime('%A'),dt.strftime("%H:%M"))



if __name__ == '__main__':
    app.run_server(debug=True)