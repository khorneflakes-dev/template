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
                dcc.Input(id='enter-id', className='enter-id', placeholder='enter user id'),
                html.Button('recommend me', id='login', n_clicks=0, className='login'),
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
    Input('login', 'n_clicks'),
    State('enter-id', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0 and value != None:
        name = engine.connect().execute(f'select name from user_names where id_user = {value};').fetchall()[0][0]
        return f'Welcome, {name}'
    else:
        return 'Welcome'

recomendacion_final = ''

# funcion para crear las cards de los restaurantes recomendados
@callback(
    Output('cards', 'children'),
    Input('login', 'n_clicks'),
    State('enter-id', 'value')    
)
def card(n_clicks, value):

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
    
    if n_clicks == 0 and value == None:
        # global recomendacion
        recomendacion = pd.read_sql('select b.name, b.address, b.latitude, b.longitude, cs.city, cs.state, b.stars, b.review_count, h.Monday, h.Tuesday, h.Wednesday, h.Thursday, h.Friday, h.Saturday, h.Sunday from business b left join business_city_state cs on b.city_state_id = cs.city_state_id left join business_hours h on b.hours_id = h.hours_id order by b.review_count desc limit 9;',
                                    con=engine)
        
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
        recomendacion_final.to_csv('./recomendacion_final.csv', index=False)
        return demoval2
    
    elif n_clicks != 0 and value != None:
        
        id_user = value
        main_cat = pd.read_parquet('main_cat.parquet.gzip')

        user_review = pd.read_sql(
            f"select id_business, stars from reviews where id_user = {id_user};",
            con=engine, index_col='id_business')
        
        user_preferences = pd.merge(user_review, main_cat, left_index=True, right_index=True)
        user_stars = user_preferences['stars'].copy()
        user_preferences.drop(columns='stars', inplace=True)
        user_stars.shape, user_preferences.transpose().shape
        user_perfil = user_preferences.transpose().dot(user_stars)
        recomendacion = (main_cat * user_perfil).sum(axis=1)/(user_perfil.sum())
        recomendacion = recomendacion.sort_values(ascending=False)

        tupla_consulta = tuple(recomendacion.keys()[:30])
        
        # global recomendacion
        recomendacion = pd.read_sql(f"select b.name, b.address, b.latitude, b.longitude, cs.city, cs.state, b.stars, b.review_count, h.Monday, h.Tuesday, h.Wednesday, h.Thursday, h.Friday, h.Saturday, h.Sunday from business b left join business_city_state cs on b.city_state_id = cs.city_state_id left join business_hours h on b.hours_id = h.hours_id where b.business_id in {tupla_consulta} order by b.review_count desc limit 9;",
                                    con=engine)
        
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
        
        # recomendacion.to_csv('recomendacion.csv', index=False)
        # recomendacion = pd.read_csv('./recomendacion.csv')
        
        
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
    if "btn-nclicks-0" == ctx.triggered_id:
        latitude = recomendacion_final['latitude'][0]
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