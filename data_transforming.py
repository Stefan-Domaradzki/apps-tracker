import pandas as pd
import re
import plotly.express as px
from dash import Dash, html, dcc


def assign_role(message):

    if not isinstance(message, str):
        print(f"Message: {message} | type: {type(message)}")
        return 'other'

    apps_and_games = pd.read_csv('./data/apps-general.csv')

    app_roles = apps_and_games.set_index('Name')['General'].to_dict()

    for app in app_roles:
        if re.search(r'\b' + re.escape(app) + r'\b', message, re.IGNORECASE):
            return app_roles[app]

    return 'other'


def clean_app_name(message):
    if not isinstance(message, str):
        print(f"Message: {message} | type: {type(message)}")
        return message

    apps_and_games = pd.read_csv('./data/apps-general.csv')
    app_roles = apps_and_games.set_index('Name')['General'].to_dict()

    for app in app_roles:
        if re.search(r'\b' + re.escape(app) + r'\b', message, re.IGNORECASE):
            return app

    return message


def clean_and_transform(data_frame):
    df = data_frame
    df = df.dropna()

    df[['date', 'time']] = df['date'].str.split('T', expand=True)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

    df = df.sort_values(by=['user', 'message', 'date', 'time'])

    result_data = []

    current_group = None

    for index, row in df.iterrows():
        if current_group is None:
            current_group = row.copy()
        elif (row['user'] == current_group['user'] and
              row['message'] == current_group['message'] and
              row['date'] == current_group['date']):
            current_group['time_spent'] += row['time_spent']
        else:
            result_data.append(current_group)
            current_group = row.copy()

    if current_group is not None:
        result_data.append(current_group)

    result_df = pd.DataFrame(result_data)

    result_df['app_name'] = result_df['message'].apply(clean_app_name)
    result_df['role'] = result_df['message'].apply(assign_role)

    result_df['time_spent'] = round(result_df['time_spent'], 0)

    # print(type(result_df))

    return result_df


def create_bar_plot(df):


    fig = px.bar(df,
                 x='user',
                 y='time_spent',
                 color='role',
                 barmode='group',
                 title='Total Time Spent in Different Activities by User',
                 labels={'time_spent': 'Total Time', 'user': 'User', 'role': 'Role'})

    fig.update_layout(
        xaxis_title='User',
        yaxis_title='Total Time',
        legend_title='Role',
        barmode='group'
    )

    return fig



def plot_top_apps_pie_chart(df, user):

    user_df = df[df['user'] == user]

    app_time = user_df.groupby('message')['time_spent'].sum()
    top_apps = app_time.nlargest(3)

    other_apps_time = app_time[~app_time.index.isin(top_apps.index)].sum()
    top_apps['Other'] = other_apps_time

    pie_data = pd.DataFrame({'App': top_apps.index, 'Time total': top_apps.values})

    pie_data['Percent'] = (pie_data['Time total'] / pie_data['Time total'].sum()) * 100

    fig = px.pie(pie_data, names='App', values='Percent',
                 title=f'{user} time in top 3 apps',
                 color_discrete_sequence=px.colors.qualitative.Plotly)

    return fig


def plot_stacked_barchart_last_7_days(df, user):
    user_df = df[df['user'] == user]

    user_df['date'] = pd.to_datetime(user_df['date'])

    end_date = user_df['date'].max()
    start_date = end_date - pd.DateOffset(days=6)
    last_7_days = pd.date_range(start=start_date, end=end_date)

    all_roles = user_df['role'].unique()
    all_days_df = pd.DataFrame({'date': last_7_days})
    all_days_df = pd.concat([all_days_df] * len(all_roles), ignore_index=True)
    all_days_df['role'] = all_roles.tolist() * len(last_7_days)

    last_7_days_df = pd.merge(all_days_df, user_df, on=['date', 'role'], how='left')

    grouped_df = last_7_days_df.groupby(['date', 'role'])['time_spent'].sum().reset_index()

    fig = px.bar(grouped_df, x='date', y='time_spent', color='role',
                 title=f'Time spent by {user} in apps by the categories (Last 7 days)',
                 labels={'date': 'Date', 'time_spent': 'Total time (sec)', 'role': 'Category'},
                 barmode='stack')

    return fig
