from dash import Dash, dcc, html, Input, Output, State, ctx
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
                
                html.P('filter by:', className='filter'),
                
                dcc.Dropdown(['All categories','Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants'], 'All categories', id='categories', className='dropdown'),
                
                dcc.RangeSlider(2005, 2021, 1, value=[2017, 2021], marks=None, tooltip={"placement": "bottom", "always_visible": True}, id='year-slider', className='range-slider')
                
            ],className='row1-col1-row1'), # filter y slider
            
            html.Div([
                
                html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.', className='map-description'),
                
                html.Div([
                    
                    html.P('CUSTOMER EXPERIENCE SATISFACTION (Percentage of reviews with stars >= 4)', className='map-title'),
                    html.Div([
                        
                        dcc.Graph(id='experience-map',style={'width': '40vw', 'height': '40vh'}, className='experience-map')
                        
                    ], className='map-container'),
                    
                ], className='experience-container')
                                
            ], className='row1-col1-row2')
                        
        ], className='row1-col1'), # primer col + descripcion
        
        html.Div([
            
            html.P('Data Driven Investing Dashboard', className='dashboard-title'),
            
            html.Div([
                
                html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.', className='heatmap-description'),
                
                html.Div([
                    html.P('ANUAL MARKET GROWTH (difference in the number of companies reviewed per year)', className='heatmap-title'),    
                    dcc.Graph(id='heatmap-trends', className='heatmap-graph',style={'width': '32vw', 'height': '40vh'})
                    
                ], className='heatmap-tendencias')
                
            ], className='row1-col2-col2')
            
        ], className='row1-col2'),
        
    ], className='business-row1'), #primera fila de business1
    
    html.Div([
        
        html.Div([
            
            html.P('TOP BUSINESS BY CUSTOMER RETENTION', className='title-retention'),
            
            dcc.Graph(id='top-retention',style={'width': '28vw', 'height': '40vh'}, className='top-retention')
            
        ], className='row1-col1'),
        
        
        html.Div([
                        
            html.P('TOP BUSINESS BY CUSTOMER SATISFACTION', className='title-satisfaction'),
            
            dcc.Graph(id='top-satisfaction', style={'width': '28vw', 'height': '40vh'}, className='top-satisfaction')
            
        ], className='row1-col2'),
        
        
        html.Div([
            dcc.RadioItems(id='word-selector', options=[
                    {'label': html.Div(['Categories'], className='option'), 'value': 'Categories'},
                    {'label': html.Div(['Attributes'], className='option'), 'value': 'Attributes'},
                ], value='Categories', className='radio-items'),
            
            dcc.Graph(id='wordcloud',style={'width': '30vw', 'height': '30vh'}),
            
            html.P('Lorem ipsum dolor sit amet consectetur. Duis ut accumsan ipsum vitae quis pellentesque iaculis potenti scelerisque. Nulla vitae nec sit rhoncus sed.')
            
        ], className='row1-col3'),
      
    ], className='business-row2 wrapper'),
     
], className = 'business1-container')



# funciones para alimentar a los contenedores de las graficas y texto interactivo 

# mapa USA

@app.callback(
    Output('experience-map', 'figure'),
    Input('year-slider', 'value'),
    Input('categories', 'value')
)
def experience_map(slider, categorie):
    conexion = engine.connect()
    if categorie == 'All categories': # estado inicial
        conexion = engine.connect()
        anio_ini = slider[0]
        anio_fin = slider[-1]

        filtro_categorie = "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')" #

        query = f"""select bce.state, r.stars , count(r.id_review) as conteo_rev
        from reviews r
        join business b on(r.id_business = b.business_id)
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in {filtro_categorie} and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        group by bce.state , r.stars
        order by bce.state, r.stars;"""
        
        query_result = conexion.execute(query)
        df_be = pd.DataFrame(query_result.fetchall())
        df_be.columns = query_result.keys()
        

        # calculate the percentage of 4 + 5 stars
        df_be_per = round(100*df_be[df_be.stars>=4].groupby(by=['state'])['conteo_rev'].agg('sum') / df_be.groupby(by=['state'])['conteo_rev'].agg('sum'), 2)
        
        fig = px.choropleth(locations=df_be_per.index.to_list(),
                        color= df_be_per.values, 
                        locationmode="USA-states",
                        scope="usa",
                        hover_name=df_be_per.index.to_list(),
                        )
        fig.update_layout({
            'plot_bgcolor': 'rgba(1, 1, 1, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        # fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(margin=dict(l=0, r=50, t=0, b=0),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        return fig
    
    elif categorie != 'All categories':
        conexion = engine.connect()
        anio_ini = slider[0]
        anio_fin = slider[-1]
    

        query = f"""select bce.state, r.stars , count(r.id_review) as conteo_rev
        from reviews r
        join business b on(r.id_business = b.business_id)
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in ('{categorie}') and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        group by bce.state , r.stars
        order by bce.state, r.stars;"""
        
        query_result = conexion.execute(query)
        df_be = pd.DataFrame(query_result.fetchall())
        df_be.columns = query_result.keys()
        

        # calculate the percentage of 4 + 5 stars
        df_be_per = round(100*df_be[df_be.stars>=4].groupby(by=['state'])['conteo_rev'].agg('sum') / df_be.groupby(by=['state'])['conteo_rev'].agg('sum'), 2)

        fig = px.choropleth(locations=df_be_per.index.to_list(),
                        color= df_be_per.values, 
                        locationmode="USA-states",
                        scope="usa",
                        hover_name=df_be_per.index.to_list(),
                        )
        fig.update_layout({
            'plot_bgcolor': 'rgba(1, 1, 1, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        # fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        

        return fig
        

# heatmap graph

@app.callback(
    Output('heatmap-trends', 'figure'),
    Input('year-slider', 'value'),
    Input('categories', 'value')
)
def heatmap_graph(slider, categorie):
    
    conexion = engine.connect()
    if categorie == 'All categories': # estado inicial

        anio_ini=slider[0]
        anio_fin=slider[-1]
        
        filtro_categorie =  "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')" #

        query = f"""select bce.state, r.year, count( distinct business_id)  as count_business
        from reviews r 
        join business b on(r.id_business = b.business_id) 
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where b.stars >=4 and r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in {filtro_categorie} and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        group by bce.state, r.year
        order by bce.state, r.year;"""

        query_result = conexion.execute(query)
        df_bb = pd.DataFrame(query_result.fetchall())
        df_bb.columns = query_result.keys()
        
        
        # calcula el porcentage de diferencia anual 
        df_bb['per_dif'] = 0.0
        for i in df_bb.index:
            mask_state = df_bb.state == df_bb.state.iloc[i]
            mask_last_year = df_bb.year == df_bb.year.iloc[i]-1
            actual_count = df_bb['count_business'].iloc[i]
            
            if df_bb[mask_state].year.min() != df_bb.year.iloc[i]:
                prev_count = df_bb['count_business'][(mask_state) & (mask_last_year)].iloc[0]
                df_bb['per_dif'].iloc[i] = round(100* (actual_count - prev_count) / prev_count , 2)

        df = df_bb.pivot(index='state' ,columns='year' , values='per_dif')
        df = df.drop(df.columns[0], axis='columns')        
        fig = px.imshow(df)
        fig.update_layout(margin=dict(l=0, r=0, t=60, b=20),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
        
               
        return fig
    
    elif categorie != 'All categories':
    
        anio_ini = slider[0]
        anio_fin = slider[-1]


        query = f"""select bce.state, r.year, count( distinct business_id)  as count_business
        from reviews r 
        join business b on(r.id_business = b.business_id) 
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where b.stars >=4 and r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie = '{categorie}' and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        group by bce.state, r.year
        order by bce.state, r.year;"""

        query_result = conexion.execute(query)
        df_bb = pd.DataFrame(query_result.fetchall())
        df_bb.columns = query_result.keys()
        
        
        # calcula el porcentage de diferencia anual 
        df_bb['per_dif'] = 0.0
        for i in df_bb.index:
            mask_state = df_bb.state == df_bb.state.iloc[i]
            mask_last_year = df_bb.year == df_bb.year.iloc[i]-1
            actual_count = df_bb['count_business'].iloc[i]
            
            if df_bb[mask_state].year.min() != df_bb.year.iloc[i]:
                prev_count = df_bb['count_business'][(mask_state) & (mask_last_year)].iloc[0]
                df_bb['per_dif'].iloc[i] = round(100* (actual_count - prev_count) / prev_count , 2)

        df = df_bb.pivot(index='state' ,columns='year' , values='per_dif')
        df = df.drop(df.columns[0], axis='columns')

        fig = px.imshow(df)
        fig.update_layout(margin=dict(l=0, r=0, t=60, b=20),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
                       
        return fig

# top 10 retencion

@app.callback(
    Output('top-retention', 'figure'),
    Input('experience-map', 'clickData'),
    Input('categories', 'value')
)
def top_retention(clk_data, categorie):
    conexion = engine.connect()
    if clk_data == None:
        if categorie == 'All categories':
            filtro_categorie =  ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
        elif categorie != 'All categories':
            filtro_categorie = f"('{categorie}')"
        
        filtro_state = ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        

        query = f"""create or replace view dif_date as
        select  r.id_user , b.name,  count(r.id_user) as reviews_per_user, timestampdiff(month, min(r.date), max(r.date)) as date_dif  
        from reviews r
        join business b on(r.id_business = b.business_id)
        join business_categories bc on (bc.categories_id = b.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where bc.p_categorie in {filtro_categorie} and bce.state in {filtro_state}
        group by r.id_user , b.name
        having reviews_per_user >1;"""

        query_result = conexion.execute(query)
        
        query = f"""select name,  avg(date_dif)  , count(id_user) as rev 
            from dif_date 
            group by name
            having rev>=10;"""

        query_result = conexion.execute(query)
        df_r = pd.DataFrame(query_result.fetchall())
        df_r.columns = query_result.keys()
        df_r = df_r.astype({'avg(date_dif)': float})

        df_r = df_r.sort_values(by='avg(date_dif)', ascending=False).head(10)
        fig = px.funnel(df_r, x='avg(date_dif)', y='name')
        fig.update_layout(yaxis_title=None)
        fig.update_layout(margin=dict(l=0, r=0, t=70, b=50),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
        return fig

    elif clk_data != None:
        
        filtro_state = clk_data["points"][0]["location"]
        
        if categorie == 'All categories':
            filtro_categorie =  ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
        elif categorie != 'All categories':
            filtro_categorie = f"('{categorie}')"
            
        
        
        query = f"""create or replace view dif_date as
        select  r.id_user , b.name,  count(r.id_user) as reviews_per_user, timestampdiff(month, min(r.date), max(r.date)) as date_dif  
        from reviews r
        join business b on(r.id_business = b.business_id)
        join business_categories bc on (bc.categories_id = b.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where bc.p_categorie in {filtro_categorie} and bce.state in ('{filtro_state}')
        group by r.id_user , b.name
        having reviews_per_user >1;"""

        query_result = conexion.execute(query)
        
        query = f"""select name,  avg(date_dif)  , count(id_user) as rev 
            from dif_date 
            group by name
            having rev>=10;"""

        query_result = conexion.execute(query)
        df_r = pd.DataFrame(query_result.fetchall())
        df_r.columns = query_result.keys()
        df_r = df_r.astype({'avg(date_dif)': float})

        df_r = df_r.sort_values(by='avg(date_dif)', ascending=False).head(10)
        fig = px.funnel(df_r, x='avg(date_dif)', y='name')
        fig.update_layout(yaxis_title=None)
        fig.update_layout(margin=dict(l=0, r=0, t=70, b=50),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')
        return fig

# # top 10 satisfaccion

@app.callback(
    Output('top-satisfaction', 'figure'),
    Input('experience-map', 'clickData'),
    Input('categories', 'value'),
    Input('year-slider', 'value')
)
def top_satisfaction(clk_data, categorie, slider):
    conexion = engine.connect()
    anio_ini = slider[0]
    anio_fin = slider[-1]


    if clk_data == None:
        filtro_state = "('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')" #
    elif clk_data != None:
        filtro_state = f"('{clk_data['points'][0]['location']}')"
    
    if categorie == 'All categories':
        filtro_categorie =  "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')"
    elif categorie != 'All categories':
        filtro_categorie = f'("{categorie}")'

    query = f"""select b.name , avg(r.stars) , count(r.id_review) as cant_rev
    from reviews r 
    join business b on(r.id_business = b.business_id) 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where r.stars >=4 and r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in {filtro_categorie} and bce.state  in {filtro_state}
    group by b.name
    order by avg(r.stars) desc;"""

    query_result = conexion.execute(query)
    business_satisfaction = pd.DataFrame(query_result.fetchall())
    business_satisfaction.columns = query_result.keys()
    
    # get the amount of business with average star greater than 4

    query = f"""select b.name , count(distinct b.address) as cant_suc
    from business b 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where bc.p_categorie in {filtro_categorie} and bce.state  in {filtro_state}
    group by b.name
    order by cant_suc desc;"""

    query_result = conexion.execute(query)
    cant_suc = pd.DataFrame(query_result.fetchall())
    cant_suc.columns = query_result.keys()
    


    # agrega columna calculada = promedio estrellas*(cant. de reviews/cant. de sucursales)
    business_satisfaction = business_satisfaction.merge(cant_suc, on='name', how='inner')
    business_satisfaction = business_satisfaction.astype({'avg(r.stars)':np.float32})
    business_satisfaction['avg_stars_rev_suc'] = business_satisfaction['avg(r.stars)'] * (business_satisfaction['cant_rev']/business_satisfaction['cant_suc'])

    df = business_satisfaction.sort_values(by=['avg_stars_rev_suc'], ascending=False).head(10).sort_values(by='avg(r.stars)', ascending=True)[['name','avg(r.stars)']]

    fig = px.bar(df, 
                x='avg(r.stars)',
                y='name', 
                orientation='h'
                
                )
    fig.update_xaxes(range=[4, 5])
    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title=None)
    fig.update_layout(margin=dict(l=0, r=0, t=70, b=50),paper_bgcolor='rgba(255, 255, 255, 0)',plot_bgcolor='rgba(255, 255, 255, 0)')

    return fig


# wordclouds
@app.callback(
    Output('wordcloud', 'figure'),
    Input('experience-map', 'clickData'),
    Input('categories', 'value'),
    Input('year-slider', 'value'),
    Input('word-selector', 'value')
    
)
def wordcloud_graph(clk_data, categorie, slider, word_selector):
    conexion = engine.connect()
    anio_ini = slider[0]
    anio_fin = slider[-1]

    if clk_data == None:
        filtro_state = "('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')" #
    elif clk_data != None:
        filtro_state = f'("{clk_data["points"][0]["location"]}")'
    
    if categorie == 'All categories':
        filtro_categorie =  "('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')"
    elif categorie != 'All categories':
        filtro_categorie = f'("{categorie}")'

    conexion = engine.connect()
   
    if word_selector == 'Categories':
        
        query = f"""select bc.categories 
        from reviews r 
        join business b on(r.id_business = b.business_id) 
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        join business_attributes ba on (b.attributes_id = ba.attributes_id)
        where r.stars >=4 and r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in {filtro_categorie} and bce.state in {filtro_state};"""

        query_result = conexion.execute(query)
        categories_CA_45 = pd.DataFrame(query_result.fetchall())
        categories_CA_45.columns = query_result.keys()
    
        texto = " ".join(re.sub("\(|\)|Restaurants|Food|Beauty & Spas|Nightlife|Active Life|Arts & Entertainment|Hotels & Travel| ","", palabras ) for palabras in categories_CA_45.categories)
        texto = re.sub("\,"," ", texto)
        
    elif word_selector == 'Attributes':
        query = f"""select ba.attributes
        from reviews r 
        join business b on(r.id_business = b.business_id) 
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        join business_attributes ba on (b.attributes_id = ba.attributes_id)
        where r.stars >=4 and r.year >={anio_ini} and r.year <={anio_fin} and bc.p_categorie in {filtro_categorie} and bce.state in {filtro_state};"""

        query_result = conexion.execute(query)
        categories_CA_45 = pd.DataFrame(query_result.fetchall())
        categories_CA_45.columns = query_result.keys()
            
        
        texto = " ".join(re.sub("\(|\,","", palabras ) for palabras in categories_CA_45.attributes)
        

    wordcloud_image = WordCloud(collocations = False, background_color="white", width=800, height=480).generate(texto)
    wordcloud_image = wordcloud_image.to_array()
    fig = px.imshow(wordcloud_image)
    
    fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        hovermode=False,
        paper_bgcolor="#F9F9FA",
        plot_bgcolor="#F9F9FA",
    )
    fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
)
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(
    #             debug=True, # enable reload when file save
    #             threaded=True, # enable dev tools
    #             dev_tools_hot_reload=True, # hot reload, only true for css design
    #             # use_reloader=True, 
    #             )
