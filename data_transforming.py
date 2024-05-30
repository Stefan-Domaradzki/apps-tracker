import pandas as pd
import re
import plotly.express as px
from dash import Dash, html, dcc


# Funkcja przypisująca rolę na podstawie nazwy aplikacji z użyciem regex
def assign_role(message):

    if(isinstance(message, str) == False):
        print(f"Message: {message} | type: {type(message)}")
        return 'other'

    # Wczytanie danych z CSV z aplikacjami i grami
    apps_and_games = pd.read_csv('./data/apps-general.csv')

    # Tworzenie słownika nazwa aplikacji -> rola
    app_roles = apps_and_games.set_index('Name')['General'].to_dict()

    for app in app_roles:
        # Użycie wyrażenia regularnego do wyszukiwania nazwy aplikacji w wiadomości
        if re.search(r'\b' + re.escape(app) + r'\b', message, re.IGNORECASE):
            return app_roles[app]

    return 'other'  # Domyślna wartość jeśli aplikacja nie zostanie znaleziona


def clean_and_transform(df):
    df[['date', 'time']] = df['date'].str.split('T', expand=True)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f')

    df = df.sort_values(by=['user', 'message', 'date', 'time'])

    # Obliczanie różnicy czasu między kolejnymi wierszami
    df['time_diff'] = df['time'].diff().fillna(pd.Timedelta(seconds=0))

    # Inicjalizacja nowej ramki danych do przechowywania wyników
    result_data = []

    # Zmienna pomocnicza do przechowywania bieżącej grupy
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

    # Dodanie ostatniej grupy
    if current_group is not None:
        result_data.append(current_group)

    # Tworzenie wynikowej ramki danych
    result_df = pd.DataFrame(result_data)

    # Usuwanie niepotrzebnych kolumn i formatowanie wyniku
    result_df = result_df.drop(columns=['time_diff'])
    result_df["total_time"] = result_df["total_time"].dt.total_seconds()
    result_df['message'] = result_df['message'].astype(str)
    result_df = result_df.dropna()
    result_df['role'] = df['message'].apply(assign_role)

    print("Successfully cleaned and transformed ")
    return result_df


def user_activity_type_bar_chart(df, user='test'):
    df['total_time'] = pd.to_numeric(df['total_time'], errors='coerce')

    # Tworzenie wykresu słupkowego
    fig = px.bar(df,
                 x='role',
                 y='total_time',
                 color='user',
                 barmode='group',
                 title='Total Time Spent i',
                 labels={'total_time': 'Total Time', 'role': 'Role', 'user': 'User'})

    # Aktualizowanie układu wykresu
    fig.update_layout(
        xaxis_title='Role',
        yaxis_title='Total Time',
        legend_title='User',
        legend=dict(title='User'),
        barmode='group'
    )

    # Wyświetlenie wykresu
    fig.show()



