from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
  
# SQLAlchemy connectable
engine = create_engine('mysql+pymysql://root:projectyelp2022@34.176.218.33/yelp_project')

# external JavaScript files
external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']

# external CSS stylesheets
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']

app = Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)


app.title = 'YELP'
server = app.server




# cuerpo de la aplicacion
# para agregar espacios usar la clase html y un metodo P, Div, Img, e.g. html.Div()

app.layout = html.Div([

    # no modificar este radioItem
    # si se necesita usar una grafica que no tenga interaccion,
    # grafica estatica, se puede usar como input este value
    html.Div(dcc.RadioItems(id='aux', value='', className='aux')),
    
    # -------------
    
    # se puede empezar a maquetar desde aqui
    
    html.H2('Titulo de mi Grafica'),
    
    html.Div([
        dcc.Graph(id='demo-graph', figure={})
    ]),

], className = 'main-container')



# funcionalidad de la aplicacion
# aqui se definen las graficas que iran en los espacios de html
# tambien la interaccion que tendran las mismas con alguna otra grafica
# o con algun boton, dropdown, input de texto o selector

@app.callback(
    Output('demo-graph', 'figure'),
    [Input('aux', 'value')]
)
def demo_graph(value):
    
    query = 'select count(id_business), year from reviews group by year order by year desc;'
    query_result = engine.connect().execute(query).fetchall()
    df = pd.DataFrame(query_result)
    df.columns = ['Business per Year', 'Year']
    
    fig = px.bar(df, 
                 x='Year',
                 y='Business per Year',
                 color='Business per Year',
                 )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)