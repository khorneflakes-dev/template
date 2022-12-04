from dash import html, Dash, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import dash

app = Dash(__name__)

df = pd.DataFrame({
    "Minimum/Maximum":["Minimum", "Maximum"],
    "Numbers of Beat": [2,60]
    })
fig = px.bar(df, x = "Minimum/Maximum", y = "Numbers of Beat", color="Minimum/Maximum")

app.layout = html.Div(
    children=[
    html.H1(children= 'HTML Dashboard Application'),
    html.Div(children= 
             '''
             Dash: Minimum/Maximum Bar Graph
             '''),
    dcc.Graph(
        id='dash_graph'
    ),
    html.Div(dcc.Input(placeholder='Enter a min value...', id='min_value', type='number', value=0)),
    html.Div(dcc.Input(placeholder='Enter a max value...', id='max_value', type='number', value=0)),
    html.Button(id='Set-val', n_clicks=0, children= 'Set'),
    html.Button(id='Refresh_current_BPM', n_clicks=0, children= 'Refresh'),
    ])
             
@app.callback(
    Output('dash_graph', 'figure'),
    State('min_value', 'value'),
    State('max_value', 'value'),
    Input('Set-val', 'n_clicks'),
    Input('Refresh_current_BPM', 'n_clicks'),

)
def update_value(min_value, max_value, *_):
    # check if a button was triggered, if not then just render both plots with 0
    ctx = dash.callback_context
    if ctx.triggered:
        # grab the ID of the button that was triggered
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # if the button that was triggered is the refresh one, then set min,max to 0
        # otherwise, the set button was triggered and so carry on normally
        if button_id == "Refresh_current_BPM":
            min_value = 0
            max_value = 0

    df = pd.DataFrame({
    "Minimum/Maximum":["Minimum", "Maximum"],
    "Numbers of Beat": [min_value, max_value]
    })
    fig = px.bar(df, x = "Minimum/Maximum", y = "Numbers of Beat", color="Minimum/Maximum")
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)