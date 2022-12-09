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
engine = create_engine(
    'mysql+pymysql://root:projectyelp2022@34.176.218.33/projectyelp', pool_size=10, max_overflow=20)

dash.register_page(__name__)


layout = html.Div([

    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),

    html.Div([

        html.Div([
            dcc.Link('Trending', href='/trending'),
        ],),
        html.Div([
            dcc.Link('Risk', href='/risk'),
        ], className='selected'),
        html.Div([
            dcc.Link('Opportunities', href='/opportunities'),
        ])
    ], className='business-menu'),

    # risk-container 1
    html.Div([

        html.Div([
            html.Div([

                html.P('filter by:', className='filter'),

                dcc.Dropdown(['All categories', 'Active Life', 'Arts & Entertainment', 'Beauty & Spas', 'Food',
                             'Hotels & Travel', 'Nightlife', 'Restaurants'], 'All categories', id='categories', className='dropdown'),

                dcc.RangeSlider(2005, 2021, 1, value=[2015, 2021], marks=None, tooltip={
                                "placement": "bottom", "always_visible": True}, id='year-slider', className='range-slider')

            ], className='row1-col1-row1'),  # filter y slider

            html.Div([

                html.P('Although California is the state with the highest customer satisfaction in all categories, it is also the state with the highest branch closures, which may be an indication of market saturation', className='risk-description'),

                html.Div([

                    dcc.Graph(
                        id='risk-map', style={'width': '50vw', 'height': '40vh'}, className='experience-map'),

                ], className='risk-container'),

            ], className='row1-col1-row2')

        ], className='row1-col1'),  # primer col + descripcion

        html.Div([

            html.P('Data Driven Risk Dashboard', className='dashboard-title'),

            html.Div([

                html.P("Among the large franchises such as Starbucks or Subway, the ones with the least risk are Taco Bell, Burger King and McDonald's, since the percentage of businesses closed and their absolute value are attractive figures for an investor",
                       className='risk-table-description'),

                html.Div(id='risk-table', className='risk-table'),

                # dcc.Graph(id='wordcloud-risk')

            ], className='row1-col2-col2')

        ], className='row1-col2'),

    ], className='risk-row1'),  # primera fila de riesgos

    html.Div([


        dcc.Graph(id='linechart', className='linechart')

    ], className='risk-row2'),

], className='business2-container')


# funciones para alimentar a los contenedores de las graficas y texto interactivo

# # mapa USA riesgos
@callback(
    Output('risk-map', 'figure'),
    Input('year-slider', 'value'),
    Input('categories', 'value')
)
def risk_map(slider, categorie):

    conexion = engine.connect()

    anio_ini = slider[0]
    anio_fin = slider[-1]

    if categorie == 'All categories':
        filtro_categorie = "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')"
    elif categorie != 'All categories':
        filtro_categorie = f'("{categorie}")'

    # /* cantidad de negocios cerrados por estado  */
    query = f"""
    select count(distinct b.business_id) as business_close, bce.state
    from reviews r 
    join business b on(r.id_business = b.business_id) 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where b.is_open = 0 and r.year >= {anio_ini} and r.year <= {anio_fin} and bc.p_categorie in {filtro_categorie}
    and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by bce.state;
    """

    query_result = conexion.execute(query)
    df_bc = pd.DataFrame(query_result.fetchall())
    df_bc.columns = query_result.keys()

    # /* cantidad total de negocios  */
    query = f"""
    select count(distinct b.business_id) as total_business, bce.state
    from reviews r 
    join business b on(r.id_business = b.business_id) 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where r.year >= {anio_ini} and r.year <= {anio_fin} and bc.p_categorie in {filtro_categorie}
    and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by bce.state
    """

    query_result = conexion.execute(query)
    df_b = pd.DataFrame(query_result.fetchall())
    df_b.columns = query_result.keys()

    df = pd.merge(df_bc, df_b, on='state', how='inner')
    df['percentage'] = round(df['business_close'] *
                             100 / df['total_business'], 2)

    fig = px.choropleth(locations=df.state,
                        color=df.percentage,
                        locationmode="USA-states",
                        scope="usa",
                        hover_name=df.state,
                        )
    fig.update_layout({
        'plot_bgcolor': 'rgba(1, 1, 1, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    # fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(margin=dict(l=0, r=50, t=0, b=0),
                      paper_bgcolor='rgba(255, 255, 255, 0)', plot_bgcolor='rgba(255, 255, 255, 0)')
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    conexion.close()
    return fig


# risk table

@callback(
    Output('risk-table', 'children'),
    Input('categories', 'value'),
)
def risk_table(categorie):

    if categorie == 'All categories':
        filtro_categorie = "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')"
    elif categorie != 'All categories':
        filtro_categorie = f'("{categorie}")'

    conexion = engine.connect()
    # categorie, state
    query = f"""
    select b.name, count(b.business_id) as top_close from business b 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where b.is_open = 0 and bc.p_categorie in {filtro_categorie}
    and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by b.name order by top_close desc;
    """

    query_result = conexion.execute(query)
    df_bc = pd.DataFrame(query_result.fetchall())
    df_bc.columns = query_result.keys()

    # /* cantidad total de negocios  */
    query = f"""
    select b.name, count(b.business_id) as total from business b 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where bc.p_categorie in {filtro_categorie}
    and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by b.name order by total desc;
    """

    query_result = conexion.execute(query)
    df_b = pd.DataFrame(query_result.fetchall())
    df_b.columns = query_result.keys()

    df = pd.merge(df_bc, df_b, on='name', how='inner')
    df['percentage'] = round(df['top_close'] * 100 / df['total'], 1)
    df['percentage'] = df['percentage'].apply(lambda x: str(x) + ' %')
    df.columns = ['Name', 'Locals Closed', 'Total Locals', 'Percentages']
    conexion.close()
    
    risk_table = dash_table.DataTable(
        df.head(10).to_dict('records'),
        [{"name": i, "id": i} for i in df.columns],
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
    return risk_table

# soft line chart


@callback(
    Output('linechart', 'figure'),
    Input('risk-map', 'clickData')
)
def risk_line(clk_data):
    if clk_data == None:
        filtro_state = "('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')"
    elif clk_data != None:
        filtro_state = f'("{clk_data["points"][0]["location"]}")'

    conexion = engine.connect()
    # /* cantidad de negocios cerrados por estado  */
    query = f"""
    create or replace view date_closed as
    select b.business_id, bc.p_categorie, max(r.year) as final_year
    from reviews r
    join business b on(r.id_business = b.business_id)
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where b.is_open=0 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
    and bce.state in {filtro_state}
    group by b.business_id;
    """
    query_result = conexion.execute(query)

    query2 = f"""
    select final_year as year , p_categorie ,count(business_id) as business_close from date_closed group by final_year, p_categorie order by p_categorie, final_year;
    """
    query2_result = conexion.execute(query2)

    df_bc = pd.DataFrame(query2_result.fetchall())
    df_bc.columns = query2_result.keys()

    # /* cantidad total de negocios  */
    query = f"""
    select r.year ,count(distinct b.business_id) as total_business, bc.p_categorie
    from reviews r 
    join business b on(r.id_business = b.business_id) 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where r.year >= 2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
    and bce.state in {filtro_state}
    group by r.year, bc.p_categorie;
    """

    query_result = conexion.execute(query)
    df_b = pd.DataFrame(query_result.fetchall())
    df_b.columns = query_result.keys()

    df = pd.merge(df_bc, df_b, left_on=['year', 'p_categorie'], right_on=[
                  'year', 'p_categorie'], how='inner')
    df['percentage'] = round(df['business_close'] *
                             100 / df['total_business'], 2)
    df.columns = ['Year', 'Categorie', 'business_close',
                  'total_business', 'Percentage']
    conexion.close()

    fig = px.line(df,
                  x="Year", y="Percentage", color='Categorie', line_shape='spline', markers=True)

    fig.update_layout(xaxis_title=None)
    fig.update_layout(margin=dict(l=0, r=0, t=70, b=50),
                      paper_bgcolor='rgba(255, 255, 255, 0)', plot_bgcolor='rgba(255, 255, 255, 1)')
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=2005, dtick=1))

    return fig
