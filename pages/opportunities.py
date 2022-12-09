from dash import Dash, dcc, html, Input, Output, State, ctx, dash_table, callback
import dash
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import math
import numpy as np
from wordcloud import WordCloud
import re

# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp', pool_size=10, max_overflow=20)

dash.register_page(__name__)


#Clases de conexiones
class conexion:
    def __init__(self, host, user,passwd,db ):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def __str__(self):
        return f"{self.user}:{self.passwd}@{self.host}/{self.db}"
        
    def __repr__(self):
        return f"host={self.host}, user={self.user}, passwd={self.passwd}, db={self.db}"


cloud = conexion('34.176.218.33','root','projectyelp2022','projectyelp')

#Se carga la tabla resumen para busquedas
engine = create_engine(f"mysql+pymysql://{cloud}")
query = ' select * from business_reviews_pob;'
query_result = engine.connect().execute(query).fetchall()
business_reviews_city_county_pob = pd.DataFrame(query_result)

df = business_reviews_city_county_pob.copy(deep=True)


layout = html.Div([
    
    html.Div([
        
        html.Div([
            dcc.Link('Trending', href='/trending'),
        ],),
        html.Div([
            dcc.Link('Risk', href='/risk'),
        ]),
        html.Div([
            dcc.Link('Opportunities', href='/opportunities'),
        ],className='selected')
    ], className='business-menu'),
    
    html.Div([
        
        html.Div([
            
            html.Div([

                html.P('filter by:', className='filter'),

                dcc.Dropdown(['All categories', 'Active Life', 'Arts & Entertainment', 'Beauty & Spas', 'Food',
                             'Hotels & Travel', 'Nightlife', 'Restaurants'], 'All categories', id='categories', className='dropdown'),

                html.P('stars less than:', className='filter'),
                dcc.Dropdown([1, 2, 3 ], 3, id='stars-dropdown',
                             className='stars-dropdown'),


            ], className='filter-area'),
            
            html.Div([
                
                html.P('Find: '),
                
                dcc.Textarea(id='text-area', placeholder='ingresar parametro' ,style={'width': '100%', 'height': 200}, className='text-area'),
                
                html.Button('Search', id='submit', n_clicks=0, className='search-button'),
                 
            ], className='find-area'),

            html.Div([

                html.P('Business opportunities by states', className='map-title'),
                
                dcc.Graph(
                    id='oop-map', style={'width': '55vw', 'height': '45vh'}, className='oop-map'),

            ], className='map-container2'),
            
        ], className='row1-col1'),
        
        html.Div([
            
            html.Div([
                
                html.P('Business opportunity', className='dashboard-title2'),
                html.P('filling unsatisfied demand', className='dashboard-title2'),
                
            ], className='dashboard-title'),
            
            html.Div([
                
                html.P('Business opportunity', className='table-title'),
                
                html.Div(id='table1', className='table1')
                
            ], className='table1'),
            
            html.Div([
                
                html.P('Adress of business opportunity',className='table-title'),
                
                html.Div(id='table2', className='table2')
                
            ], className='table2'),
            
        ], className='row1-col2')
        
    ], className='row1'),
    
    html.Div([
        
        html.P('Business opportunities by categories', className='treemap-description'),
        dcc.Graph(id='treemap', className='treemap',style={'width': '95vw', 'height': '40vh'}),
        
        
    ], className='row2'),

], className='opp-container')

# definiendo la logica de la aplicacion


#Filtro por estrellas
def filtro_estrellas(df,cantidad_estrellas):   
    df = df[df['stars']<=cantidad_estrellas]
    return df

#Flitro por categorias principales
def filtro_cat_principal(df,cat_primaria_selec):
    cat_primaria = ['Food', 'Arts & Entertainment', 'Beauty & Spas', 'Restaurants','Nightlife', 'Active Life', 'Hotels & Travel']
    if cat_primaria_selec in cat_primaria:
        categoria = cat_primaria_selec
        df = df[df['p_categorie'] == categoria]
    return df

#Filtro por categoria secundaria
def filtro_cat_secundaria(df,palabras_busqueda):
    cat_secund = str(palabras_busqueda)  
    df = df[df['categories'].str.contains(cat_secund,case=False, regex=False,na=False)]
    return df

#Flitro por estado
def filtro_por_estado(df,estado):
    estados = ['PA', 'NV', 'LA', 'TN', 'FL', 'CA', 'MO', 'AZ', 'IN', 'NJ', 'IL','ID', 'DE']
    if estado in estados:
        df = df[df['state'] == estado]
    return df

#Filtro global
def filtro_global(df,estrellas = None,cat_principal = None,cat_secundaria = None,estado = None):
    if estrellas != None:
        df  = filtro_estrellas(df,estrellas)
    if cat_principal != None:
        df  = filtro_cat_principal(df,cat_principal) #['Food', 'Arts & Entertainment', 'Beauty & Spas', 'Restaurants','Nightlife', 'Active Life', 'Hotels & Travel']
    if cat_secundaria != None:
        df  = filtro_cat_secundaria(df,cat_secundaria)   #'Sport'  #'Photographers' #'Sushi Bars' .....
    if estado != None:
        df  = filtro_por_estado(df,estado)        # ['PA', 'NV', 'LA', 'TN', 'FL', 'CA', 'MO', 'AZ', 'IN', 'NJ', 'IL','ID', 'DE']
    df.sort_values('rev_cat_pob',ascending=False,inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#filtros #1 : Si no se escoge nada presenta todos los estados y escoge entre todas las categorias primarias y para tres estrellas
def data_grafica_todos_estados(df,estrellas = 3,cat_principal = None,cat_secundaria = None,estado = None):
    if estado:
        df_estados = filtro_global(df,estrellas,cat_principal,cat_secundaria,estado)
    else:
        df_estados =pd.DataFrame(columns=df.columns)            
        estados = ['PA', 'NV', 'LA', 'TN', 'FL', 'CA', 'MO', 'AZ', 'IN', 'NJ', 'IL','ID', 'DE']
        for estado in estados:
            row = filtro_global(df,estrellas,cat_principal,cat_secundaria,estado).loc[0,:]
            df_estados = df_estados.append(row,ignore_index=True)
    df_estados.sort_values('rev_cat_pob',ascending=False,inplace=True)
    df_estados.reset_index(drop=True, inplace=True)
    df_estados = df_estados.head(10)
    return df_estados


@callback(
    Output('oop-map', 'figure'),
    Input('stars-dropdown', 'value'),
    Input('categories', 'value'),
    Input('submit', 'n_clicks'),
    State('text-area', 'value'),
    Input('oop-map', 'clickData')
)
def depliegue_mapa(stars, Pcategories, n_clicks, text_area,clk_data):
    
    # if n_clicks > 0 and text_area != None:
    #     grafica = data_grafica_todos_estados(df,stars,Pcategories)
    # else:
    #     grafica = data_grafica_todos_estados(df,stars,Pcategories,text_area)
    if clk_data == None:
        filtro_state = None
        print(filtro_state)
    elif clk_data != None:
        filtro_state = clk_data['points'][0]['location']
        
    grafica = data_grafica_todos_estados(df,stars,Pcategories, None, filtro_state)
        
    df_grafica = pd.Series(list(grafica['rev_cat_pob']),index=grafica['state'])
    fig = px.choropleth(locations=df_grafica.index.to_list(),
                    color= df_grafica.values, 
                    locationmode="USA-states",
                    scope="usa",
                    hover_name= list(grafica.loc[:,'state_name'])
                    )
    fig.update_layout(margin=dict(l=30, r=30, t=70, b=30),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    return fig


# table 1

@callback(
    Output('table1', 'children'),
    Input('stars-dropdown', 'value'),
    Input('categories', 'value'),
    Input('oop-map', 'clickData')
)
def despligue_ciudades(stars, Pcategories, clk_data):
    
    if clk_data == None:
        filtro_state = None
        print(filtro_state)
    elif clk_data != None:
        filtro_state = clk_data['points'][0]['location']
    
    grafica = data_grafica_todos_estados(df,stars,Pcategories, None, filtro_state)
    if grafica.loc[0,'state'] == grafica.loc[1,'state']: 
        tabla = grafica[['city','name','rev_cat_pob']]
        tabla.columns = ['City', 'Name', 'Rev Cat Pob']
    else:
        tabla = grafica[['state_name','city','name','rev_cat_pob']]
        tabla.columns = ['State', 'City', 'Name', 'Rev Cat Pob']

    tabla['Rev Cat Pob'] = [round(num,2) for num in tabla['Rev Cat Pob']]
    
   
    table1 = dash_table.DataTable(
        tabla.head().to_dict('records'),
        [{"name": i, "id": i} for i in tabla.columns],
        style_header={
            'backgroundColor': '#2A2A2A',
            'color': 'white'
        },
        style_data={
            'backgroundColor': '#FFFFFF',
            'color': '#2a2a2a',
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        style_table={
            'maxWidth': '40vw'
        },
        cell_selectable=False
    )
    
    return table1

# table 2

@callback(
    Output('table2', 'children'),
    Input('stars-dropdown', 'value'),
    Input('categories', 'value'),
    Input('oop-map', 'clickData')
)
def despligue_direcciones(stars, Pcategories, clk_data):
    
    if clk_data == None:
        filtro_state = None

    elif clk_data != None:
        filtro_state = clk_data['points'][0]['location']
        
    grafica = data_grafica_todos_estados(df,stars,Pcategories,None,filtro_state)
    id = tuple(grafica['business_id'])
    engine = create_engine(f"mysql+pymysql://{cloud}")
    query = f"""select * from business as b where business_id in {id} ;"""
    query_result = engine.connect().execute(query).fetchall()
    direccion = pd.DataFrame(query_result)
    tabla = direccion[['name','address']]
    
    tabla.columns = ['Name', 'Address']
    table2 = dash_table.DataTable(
        tabla.head().to_dict('records'),
        [{"name": i, "id": i} for i in tabla.columns],
        style_header={
            'backgroundColor': '#2A2A2A',
            'color': 'white'
        },
        style_data={
            'backgroundColor': '#FFFFFF',
            'color': '#2a2a2a',
        },
        cell_selectable=False
    )
    
    return table2

# treemap

@callback(
    Output('treemap', 'figure'),
    Input('stars-dropdown', 'value'),
    Input('categories', 'value'),
    Input('oop-map', 'clickData')
)
    
def despliegue_treemap(stars, Pcategories, clk_data):
    
    if clk_data == None:
        filtro_state = None

    elif clk_data != None:
        filtro_state = clk_data['points'][0]['location']
    
    grafica = data_grafica_todos_estados(df,stars,Pcategories, None, filtro_state)
    fig = px.treemap(grafica,values= 'rev_cat_pob', path=['p_categorie','name','categories'])
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=0, r=50, t=0, b=0),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
    fig.update_traces(root_color="lightgrey")
    return fig
