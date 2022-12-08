import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

animals = ['Fox', 'Deer', 'Elephant', 'Cat', 'Dog']


app.layout = html.Div([
    html.Div([
        html.Button(those, id='my-button-events-example', value=those) for those in animals
    ]),
    html.Div([
        html.H4(id='button'),
    ])
])


@app.callback(
    Output('button', 'children'),
    [Input('my-button-events-example', 'value')],
    #state=[State('my-input', 'value')]
)
def test(value):
	return 'You pressed "{}"'.format(value)


if __name__ == '__main__':
    app.run_server()