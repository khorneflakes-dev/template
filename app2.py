from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


app1 = Dash(requests_pathname_prefix="/app1/")
app1.layout = html.Div("Hello, Dash app 1!")

app2 = Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Hello, Dash app 2!")

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server, "/app2": app2.server},
)

if __name__ == "__main__":
    run_simple("localhost", 8050, application,
               use_reloader=True, use_debugger=True, use_evalex=True)