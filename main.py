"""
    TODO: 1. Узнать при помощи каких библиотек можно делать интерфейс.
          2. Определиться с запросами (что будем предоставлять). Список 2 - 4 вида
    1. Фильтрация по различным параметрам
    2.
"""

import pandas as pd

'''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
'''
movies = pd.DataFrame(pd.read_csv('movies_test.csv', usecols=['release_date', 'budget', 'revenue']))
''' 
marvel = movies['production_companies'] == 'Marvel Studios'
marvel_data = pd.DataFrame(movies.loc[marvel, ["title"]])
print(list(marvel_data.to_records()))
'''

# Окупаемость
movies['release_year'] = pd.DatetimeIndex(movies['release_date']).year
movies = movies[(movies.budget != 0) & (movies.revenue != 0)]
movies['payback'] = (movies['revenue'] - movies['budget']) / movies['budget']
print(movies)
movies = movies.groupby(['release_year'])['payback'].mean()
print(movies)
# ---------------------------------------------------------------------------
