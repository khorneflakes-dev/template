import dash
from dash import html, dcc, callback, Input, Output, State, ctx
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import math
import pandas as pd


# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')


dash.register_page(__name__)

layout = html.Div([
    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),

    html.Div([
        
        html.Div([
            html.Div([
                html.Div([
                    html.P('Welcome', id='welcome', className='welcome-title')
                ],className='header-row1'),
                html.Div([
                    html.P('Discover new flavors', className='welcome-description'),
                    html.Div([
                        html.P(id='options'), #dropdown pendiente
                        html.Img(src='') #svg de flecha pendiente
                    ], className='options')
                ],className='header-row2'),
            ], className='header'),
            
            html.Div(id='cards'
                # html.Div([
                #     html.P(id='restaurant-name', className='restaurant-name'),
                #     html.Div([
                #         html.Div([
                            
                #         ],className='atention-days'),
                #         html.Div([
                            
                #         ], className='atention-hours')
                #     ], className='atention'),
                #     html.P(id='address', className='address'),
                #     html.P(id='city-state'),
                #     html.Div([
                #         html.Div([
                            
                #         ], className='stars'),
                #         html.P(id='n-reviews')
                #     ], className='rating')
                # ], className='card')
            , className='cards')
        ], className='col1'),
        
        html.Div([
            html.Div([
                # dcc.Input(id='enter-id', className='enter-id', placeholder='enter user id'),
                # html.Button('recommend me', id='login', n_clicks=0, className='login'),
                dcc.Dropdown([672291, 762612, 1241051, 1870361, 1172061, 688050, 1077256, 351604, 662185, 1793565],672291, id='user-dropdown')
            ], className='login-container'),
            
            html.Div(id='iframe'
                # html.Iframe(id='iframe-map',src='https://www.google.com/maps/embed/v1/place?key=AIzaSyBKqlE-X4gVVz0YNXpsJcMuaFEfqhkHIio&q=36.151387,-86.796603',
                #             style={'width':"1500", 'height':"1080", 'style':"border:0", 'loading':"lazy", 'referrerpolicy':"no-referrer-when-downgrade"}, className='iframe')   
            , className='map'),
        ],className='col2'),
        
    ], className='users-container'),  

], className = 'main-container')



# funcion para validar el id_user
@callback(
    Output('welcome', 'children'),
    # Input('login', 'n_clicks'),
    # State('enter-id', 'value'),
    Input('user-dropdown', 'value')
)
def update_output(value):
    if value != None:
        name = engine.connect().execute(f'select name from user_names where id_user = {value};').fetchall()[0][0]
        return f'Welcome, {name}'
    else:
        return 'Welcome'

recomendacion_final = ''

# funcion para crear las cards de los restaurantes recomendados
@callback(
    Output('cards', 'children'),
    Input('user-dropdown', 'value')
)
def card(value):
    def stars(value):
        decimal, entero = math.modf(value)
        lista = ''
        for i in list(range(int(entero))):
            lista += 'A'
        if decimal != 0:
            lista += 'B'

        for i in list(range(5)):
            lista += 'C'

        return lista[:5]
    def hour_format(value):
        from datetime import datetime
        from time import strptime
        if value == '0':
            return '00:00-00:00'
        else:
            horas = value.split('-')
            hora1 = datetime.strptime(horas[0], '%H:%M').time()
            hora2 = datetime.strptime(horas[-1], '%H:%M').time()
            nuevaHora = ':'.join((str(hora1)).split(':')[:-1]) + '-' + ':'.join((str(hora2)).split(':')[:-1])
            return nuevaHora
        
    engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')
    
    global recomendacion_final
    
    if value == None:
        recomendacion = pd.read_csv('./prediccion.csv')
        
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            recomendacion[i] = recomendacion[i].apply(lambda x: hour_format(x))
            


        recomendacion['estrellas'] = recomendacion['stars'].apply(lambda x: stars(x))
        
        
        demoval2 = html.Div([

            html.Div([
                html.P(recomendacion.iloc[i,:]['name'], className='restaurant-name'),
                html.Div([
                    html.Div([
                        html.P('Monday:'),
                        html.P('Tuesday:'),
                        html.P('Wednesday:'),
                        html.P('Thursday:'),
                        html.P('Friday:'),
                        html.P('Saturday:'),
                        html.P('Sunday:')
                    ], className='atention-days'),
                    html.Div([
                        html.P(recomendacion.iloc[i, :]['Monday']),
                        html.P(recomendacion.iloc[i, :]['Tuesday']),
                        html.P(recomendacion.iloc[i, :]['Wednesday']),
                        html.P(recomendacion.iloc[i, :]['Thursday']),
                        html.P(recomendacion.iloc[i, :]['Friday']),
                        html.P(recomendacion.iloc[i, :]['Saturday']),
                        html.P(recomendacion.iloc[i, :]['Sunday'])
                    ], className='atention-hours')
                ], className='atention'),
                html.Div([
                    html.P(recomendacion.iloc[i, :]['address'], className='address'),
                    html.P(recomendacion.iloc[i, :]['city']+', ' + recomendacion.iloc[i, :]['state'], className='city-state'),
                    html.Button(f'show map', id=f'btn-nclicks-{i}', n_clicks=0),
                ], className='direccion'),
                html.Div([
                    html.Div([
                        
                        html.Img(src=f'./assets/star{j}.png', className='star1')
                        for j in recomendacion.iloc[i, :]['estrellas']
                        
                    ], className='stars'),
                    
                    html.P(str(recomendacion.iloc[i, :]['review_count']) + ' reviews', className='review-count'),
                ], className='rating')
            ], className='card')


            for i in list(range(len(recomendacion)))
        ], className='cards2')
        engine.dispose()
        
        recomendacion_final = recomendacion
        return demoval2
    
    elif value != None:
        
        df_predicciones = pd.read_csv('./predicciones.csv')
        
        recomendacion = df_predicciones[df_predicciones.id_user == value]
        
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            recomendacion[i] = recomendacion[i].apply(lambda x: hour_format(x))
        
        def stars(value):
            decimal, entero = math.modf(value)
            lista = ''
            for i in list(range(int(entero))):
                lista += 'A'
            if decimal != 0:
                lista += 'B'
            for i in list(range(5)):
                lista += 'C'
            return lista[:5]

        recomendacion['estrellas'] = recomendacion['stars'].apply(lambda x: stars(x))
        recomendacion.drop('id_user', axis=1, inplace=True)
        demoval = html.Div([

            html.Div([
                html.P(recomendacion.iloc[i,:]['name'], className='restaurant-name'),
                html.Div([
                    html.Div([
                        html.P('Monday:'),
                        html.P('Tuesday:'),
                        html.P('Wednesday:'),
                        html.P('Thursday:'),
                        html.P('Friday:'),
                        html.P('Saturday:'),
                        html.P('Sunday:')
                    ], className='atention-days'),
                    html.Div([
                        html.P(recomendacion.iloc[i, :]['Monday']),
                        html.P(recomendacion.iloc[i, :]['Tuesday']),
                        html.P(recomendacion.iloc[i, :]['Wednesday']),
                        html.P(recomendacion.iloc[i, :]['Thursday']),
                        html.P(recomendacion.iloc[i, :]['Friday']),
                        html.P(recomendacion.iloc[i, :]['Saturday']),
                        html.P(recomendacion.iloc[i, :]['Sunday'])
                    ], className='atention-hours')
                ], className='atention'),
                html.Div([
                    html.P(recomendacion.iloc[i,:]['address'], className='address'),
                    html.P(recomendacion.iloc[i,:]['city']+', '+recomendacion.iloc[i,:]['state'], className='city-state'),
                    html.Button(f'show map', id=f'btn-nclicks-{i}', n_clicks=0),
                ], className='direccion'),
                html.Div([
                    html.Div([
                        
                        html.Img(src=f'./assets/star{j}.png', className='star1')
                        for j in recomendacion.iloc[i, :]['estrellas']
                        
                    ], className='stars'),
                    html.P(str(recomendacion.iloc[i, :]['review_count']) + ' reviews', className='review-count'),
                    
                ], className='rating')
            ], className='card')


            for i in list(range(len(recomendacion)))
        ], className='cards2')
        engine.dispose()
        
        
        recomendacion_final = recomendacion
        
        return demoval


@callback(
    Output('iframe', 'children'),
    Input('btn-nclicks-0', 'n_clicks'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks'),
    Input('btn-nclicks-7', 'n_clicks'),
    Input('btn-nclicks-8', 'n_clicks'),

)
def displayBack(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9):
    
    latitude = ''
    longitude = ''
    if  "btn-nclicks-0"  == ctx.triggered_id:
        latitude  = recomendacion_final['latitude'][0]
        longitude = recomendacion_final['longitude'][0]
    elif "btn-nclicks-1" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][1]
        longitude = recomendacion_final['longitude'][1]
    elif "btn-nclicks-2" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][2]
        longitude = recomendacion_final['longitude'][2]
    elif "btn-nclicks-3" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][3]
        longitude = recomendacion_final['longitude'][3] 
    elif "btn-nclicks-4" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][4]
        longitude = recomendacion_final['longitude'][4]
    elif "btn-nclicks-5" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][5]
        longitude = recomendacion_final['longitude'][5]
    elif "btn-nclicks-6" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][6]
        longitude = recomendacion_final['longitude'][6]
    elif "btn-nclicks-7" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][7]
        longitude = recomendacion_final['longitude'][7]
    elif "btn-nclicks-8" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][8]
        longitude = recomendacion_final['longitude'][8]


    iframe = html.Iframe(id='iframe-map',src=f'https://www.google.com/maps/embed/v1/place?key=AIzaSyBKqlE-X4gVVz0YNXpsJcMuaFEfqhkHIio&q={latitude},{longitude}&maptype=satellite',
                            style={'width':"1500", 'height':"1080", 'style':"border:0", 'loading':"lazy", 'referrerpolicy':"no-referrer-when-downgrade"}, className='iframe')
    return iframe