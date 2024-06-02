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


def clean_and_transform(df):
    df[['date', 'time']] = df['date'].str.split('T', expand=True)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

    df = df.sort_values(by=['user', 'message', 'date', 'time'])

    df['time_diff'] = df['time'].diff().fillna(pd.Timedelta(seconds=0))

    result_data = []

    current_group = None

    for index, row in df.iterrows():
        if current_group is None:
            current_group = row.copy()
            current_group['total_time'] = pd.Timedelta(seconds=0)
        elif (row['user'] == current_group['user'] and
              row['message'] == current_group['message'] and
              row['date'] == current_group['date']):
            current_group['total_time'] += row['time_diff']
        else:
            result_data.append(current_group)
            current_group = row.copy()
            current_group['total_time'] = pd.Timedelta(seconds=0)

    if current_group is not None:
        result_data.append(current_group)

    result_df = pd.DataFrame(result_data)

    result_df = result_df.drop(columns=['time_diff'])
    result_df["total_time"] = result_df["total_time"].dt.total_seconds()
    result_df['message'] = result_df['message'].astype(str)
    result_df = result_df.dropna()
    result_df['role'] = df['message'].apply(assign_role)

    print("Successfully cleaned and transformed ")
    return result_df


def create_bar_plot(df):

    df['total_time'] = pd.to_numeric(df['total_time'], errors='coerce')

    fig = px.bar(df,
                 x='user',
                 y='total_time',
                 color='role',
                 barmode='group',
                 title='Total Time Spent in Different Activities by User',
                 labels={'total_time': 'Total Time', 'user': 'User', 'role': 'Role'})

    fig.update_layout(
        xaxis_title='User',
        yaxis_title='Total Time',
        legend_title='Role',
        barmode='group'
    )

    return fig


def plot_top_apps_pie_chart(df, user):

    user_df = df[df['user'] == user]

    app_time = user_df.groupby('message')['total_time'].sum()
    top_apps = app_time.nlargest(3)

    other_apps_time = app_time[~app_time.index.isin(top_apps.index)].sum()
    top_apps['Inne'] = other_apps_time

    pie_data = pd.DataFrame({'Aplikacja': top_apps.index, 'Całkowity czas': top_apps.values})

    pie_data['Procent'] = (pie_data['Całkowity czas'] / pie_data['Całkowity czas'].sum()) * 100

    fig = px.pie(pie_data, names='Aplikacja', values='Procent',
                 title=f'Procentowy udział czasu w aplikacjach przez {user}',
                 color_discrete_sequence=px.colors.qualitative.Plotly)

    return fig


def plot_stacked_barchart_last_7_days(df, user):
    user_df = df[df['user'] == user]

    user_df['date'] = pd.to_datetime(user_df['date'])

    end_date = user_df['date'].max()
    start_date = end_date - pd.DateOffset(days=6)
    last_7_days = pd.date_range(start=start_date, end=end_date)

    # role wczytywane aby w przyszlosci moc rozszrzyc o inne
    all_roles = user_df['role'].unique()
    all_days_df = pd.DataFrame({'date': last_7_days})
    all_days_df = pd.concat([all_days_df] * len(all_roles), ignore_index=True)
    all_days_df['role'] = all_roles.tolist() * len(last_7_days)

    last_7_days_df = pd.merge(all_days_df, user_df, on=['date', 'role'], how='left')

    grouped_df = last_7_days_df.groupby(['date', 'role'])['total_time'].sum().reset_index()

    fig = px.bar(grouped_df, x='date', y='total_time', color='role',
                 title=f'Czas spędzony w różnych kategoriach przez {user} (Ostatnie 7 dni)',
                 labels={'date': 'Data', 'total_time': 'Całkowity czas (s)', 'role': 'Kategoria'},
                 barmode='stack')

    return fig
