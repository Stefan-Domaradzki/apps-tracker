# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


from tracker_consumer import window_consumer_single_topic

from data_transforming import clean_and_transform
from data_transforming import user_activity_type_bar_chart
from data_transforming import create_bar_plot

app = Dash(__name__)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = window_consumer_single_topic(topic='used_apps_all_users3')
df = clean_and_transform(df)

#fig = user_activity_type_bar_chart(df, user='Stefan')
fig = create_bar_plot(df)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
