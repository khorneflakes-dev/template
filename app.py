from dash import Dash, dcc, html, Input, Output, State, ctx
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import math

# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp')

app = Dash(__name__)

app.title = 'YELP'
server = app.server



app.layout = html.Div([
    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),
        html.Div(id='demo'),
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
            
            html.Div([
                html.Iframe(id='iframe-map',src='https://www.google.com/maps/embed/v1/place?key=AIzaSyBKqlE-X4gVVz0YNXpsJcMuaFEfqhkHIio&q=36.151387,-86.796603',
                            style={'width':"1500", 'height':"1080", 'style':"border:0", 'loading':"lazy", 'referrerpolicy':"no-referrer-when-downgrade"}, className='iframe')   
            ], className='map'),
        ],className='col2'),
        
    ], className='users-container'),  
    

], className = 'main-container')



# funcion para validar el id_user
@app.callback(
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


# funcion para crear las cards de los restaurantes recomendados
@app.callback(
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
    if n_clicks == 0 and value == None:
        recomendacion2 = pd.read_sql('select b.name, b.address, b.latitude, b.longitude, cs.city, cs.state, b.stars, b.review_count, h.Monday, h.Tuesday, h.Wednesday, h.Thursday, h.Friday, h.Saturday, h.Sunday from business b left join business_city_state cs on b.city_state_id = cs.city_state_id left join business_hours h on b.hours_id = h.hours_id order by b.review_count desc limit 9;',
                                    con=engine)
        
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            recomendacion2[i] = recomendacion2[i].apply(lambda x: hour_format(x))
            
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

        recomendacion2['estrellas'] = recomendacion2['stars'].apply(lambda x: stars(x))
     
        
        demoval2 = html.Div([

            html.Div([
                html.P(recomendacion2.iloc[i,:]['name'], className='restaurant-name'),
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
                        html.P(recomendacion2.iloc[i, :]['Monday']),
                        html.P(recomendacion2.iloc[i, :]['Tuesday']),
                        html.P(recomendacion2.iloc[i, :]['Wednesday']),
                        html.P(recomendacion2.iloc[i, :]['Thursday']),
                        html.P(recomendacion2.iloc[i, :]['Friday']),
                        html.P(recomendacion2.iloc[i, :]['Saturday']),
                        html.P(recomendacion2.iloc[i, :]['Sunday'])
                    ], className='atention-hours')
                ], className='atention'),
                html.Div([
                    html.P(recomendacion2.iloc[i, :]['address'], className='address'),
                    html.P(recomendacion2.iloc[i, :]['city']+', ' + recomendacion2.iloc[i, :]['state'], className='city-state'),
                    html.Button(f'ver mapa', id=f'btn-nclicks-{i}', n_clicks=0),
                ], className='direccion'),
                html.Div([
                    html.Div([
                        
                        html.Img(src=f'./assets/star{j}.png', className='star1')
                        for j in recomendacion2.iloc[i, :]['estrellas']
                        
                    ], className='stars'),
                    
                    html.P(str(recomendacion2.iloc[i, :]['review_count']) + ' reviews', className='review-count'),
                ], className='rating')
            ], className='card')


            for i in list(range(len(recomendacion2)))
        ], className='cards2')
        engine.dispose()
        return demoval2
    
    elif n_clicks > 0 and value != None:
            
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
        recomendacion1 = pd.read_sql(f"select b.name, b.address, b.latitude, b.longitude, cs.city, cs.state, b.stars, b.review_count, h.Monday, h.Tuesday, h.Wednesday, h.Thursday, h.Friday, h.Saturday, h.Sunday from business b left join business_city_state cs on b.city_state_id = cs.city_state_id left join business_hours h on b.hours_id = h.hours_id where b.business_id in {tupla_consulta} order by b.review_count desc limit 9;",
                                    con=engine)
        
        for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            recomendacion1[i] = recomendacion1[i].apply(lambda x: hour_format(x))
        
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

        recomendacion1['estrellas'] = recomendacion1['stars'].apply(lambda x: stars(x))
        
        # recomendacion1.to_csv('recomendacion1.csv', index=False)
        # recomendacion1 = pd.read_csv('./recomendacion1.csv')
        
        
        demoval = html.Div([

            html.Div([
                html.P(recomendacion1.iloc[i,:]['name'], className='restaurant-name'),
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
                        html.P(recomendacion1.iloc[i, :]['Monday']),
                        html.P(recomendacion1.iloc[i, :]['Tuesday']),
                        html.P(recomendacion1.iloc[i, :]['Wednesday']),
                        html.P(recomendacion1.iloc[i, :]['Thursday']),
                        html.P(recomendacion1.iloc[i, :]['Friday']),
                        html.P(recomendacion1.iloc[i, :]['Saturday']),
                        html.P(recomendacion1.iloc[i, :]['Sunday'])
                    ], className='atention-hours')
                ], className='atention'),
                html.Div([
                    html.P(recomendacion1.iloc[i,:]['address'], className='address'),
                    html.P(recomendacion1.iloc[i,:]['city']+', '+recomendacion1.iloc[i,:]['state'], className='city-state'),
                    html.Button(f'ver mapa', id=f'btn-nclicks-{i}', n_clicks=0),
                ], className='direccion'),
                html.Div([
                    html.Div([
                        
                        html.Img(src=f'./assets/star{j}.png', className='star1')
                        for j in recomendacion1.iloc[i, :]['estrellas']
                        
                    ], className='stars'),
                    html.P(str(recomendacion1.iloc[i, :]['review_count']) + ' reviews', className='review-count'),
                    
                ], className='rating')
            ], className='card')


            for i in list(range(len(recomendacion1)))
        ], className='cards2')
        engine.dispose()
        
        return demoval


@app.callback(
    Output('demo', 'children'),
    Input('btn-nclicks-0', 'n_clicks'),
    Input('btn-nclicks-1', 'n_clicks'),
)
def displayBack(btn1, btn2):
    msg = 'estado inicial'
    if "btn-nclicks-0" == ctx.triggered_id:
        return 'boton 1 presionado'
    elif "btn-nclicks-1" == ctx.triggered_id:
        return 'boton 2 presionado'
    else:
        return msg


if __name__ == '__main__':
    app.run_server(debug=True)
