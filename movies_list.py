import pandas as pd


class MoviesList:
    def __init__(self):
        self.df = pd.read_csv("movies.csv", delimiter=",", encoding="iso-8859-1", dtype={'title': str, 'genres': str,
                                                                                    'original_language': str,
                                                                                    'budget': float, 'revenue': float,
                                                                                    'runtime': float,
                                                                                    'vote_average': float,
                                                                                    'vote_count': float,
                                                                                    'keywords': str},
                         parse_dates=['release_date'], dayfirst=True, on_bad_lines='skip')
        self.df = self.df[['title', 'genres', 'original_language', 'release_date', 'budget', 'revenue', 'runtime',
                 'vote_average', 'vote_count', 'keywords']]
        self.total_size = len(self.df)
        self.df = self.df.drop_duplicates(subset=['title', 'release_date'])
        self.df['release_date'] = pd.to_datetime(self.df['release_date'], format='%d.%m.%Y', errors='coerce').dt.date
        self.df['genres'].fillna('', inplace=True)
        self.df['keywords'].fillna('', inplace=True)
        self.filtered_df = self.df.copy()

    @property
    def size(self):
        return self.total_size

    @property
    def filtered_size(self):
        return len(self.filtered_df)
