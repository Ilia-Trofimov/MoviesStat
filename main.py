"""
    TODO: 1. Узнать при помощи каких библиотек можно делать интерфейс.
          2. Определиться с запросами (что будем предоставлять). Список 2 - 4 вида
    1. Фильтрация по различным параметрам
    2.
"""

import pandas as pd
import matplotlib.pyplot as plot

from main_window import MainWindow

pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

movies = pd.DataFrame(pd.read_csv('movies.csv', usecols=['release_date', 'budget', 'revenue', 'vote_count']))
''' 
marvel = movies['production_companies'] == 'Marvel Studios'
marvel_data = pd.DataFrame(movies.loc[marvel, ["title"]])
print(list(marvel_data.to_records()))
'''

# Окупаемость
"""
movies['release_year'] = pd.DatetimeIndex(movies['release_date']).year
movies['vote_count'] = movies['vote_count'].astype(float)
movies = movies[(movies.budget != 0) & (movies.revenue != 0) & (movies.vote_count > 900)]
movies['payback'] = (movies['revenue'] - movies['budget']) / movies['budget']
print(movies.size)
movies = pd.DataFrame(movies.groupby(['release_year'])['payback'].mean())
print(movies)

plot.bar(movies['release_year'], movies['payback'])
plot.show()
"""
# ---------------------------------------------------------------------------

MainWindow()