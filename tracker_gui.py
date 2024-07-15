from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio

from kafka_connector import window_consumer_single_topic, all_users, window_consumer_2
from data_transforming import clean_and_transform
from data_transforming import create_bar_plot, plot_top_apps_pie_chart, plot_stacked_barchart_last_7_days

app = Dash(__name__)

pio.templates["light"] = pio.templates["plotly_white"]
pio.templates["light"].layout.plot_bgcolor = 'rgba(255, 255, 255, 1)'
pio.templates["light"].layout.paper_bgcolor = 'rgba(245, 245, 245, 1)'
pio.templates["light"].layout.font.color = 'rgba(50, 50, 50, 1)'
pio.templates["light"].layout.colorway = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

#df = window_consumer_single_topic(topic='used_apps_all_users3')
df = window_consumer_2(topic='apps3')
df = clean_and_transform(df)

users = all_users(df)

app.layout = html.Div(style={'backgroundColor': '#FFFFFF', 'color': '#000000'}, children=[
    html.H1(children='Apps Tracker', style={'color': '#000000'}),

    html.Div(children='166642 Domaradzki Stefan Lab 1', style={'color': '#333333'}),
    html.Div(children='Usługi Sieciowe w biznesie P1', style={'color': '#333333'}),

    dcc.Graph(
        id='example-graph'
    ),

    html.H2(children='Wybierz użytkownika', style={'color': '#000000'}),

    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': user, 'value': user} for user in users],
        value=users[0],
        style={'backgroundColor': '#FFFFFF', 'color': '#000000', 'border': '1px solid #CCCCCC'}
    ),

    dcc.Graph(
        id='pie-chart'
    ),

    dcc.Graph(
        id='stacked-bar-chart'
    )
])


@app.callback(
    Output('example-graph', 'figure'),
    [Input('user-dropdown', 'value')]
)
def update_graph(selected_user):
    fig = create_bar_plot(df)
    fig.update_layout(template='light')
    return fig


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('user-dropdown', 'value')]
)
def update_pie_chart(selected_user):
    fig = plot_top_apps_pie_chart(df, selected_user)

    # Zastosowanie szablonu light do wykresu
    fig.update_layout(template='light')
    return fig


@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('user-dropdown', 'value')]
)
def update_stacked_bar_chart(selected_user):
    fig = plot_stacked_barchart_last_7_days(df, selected_user)

    fig.update_layout(template='light')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
