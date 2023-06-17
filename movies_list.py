import pandas as pd


class MoviesList:
    def __init__(self):
        self.df = pd.read_csv("movies1.csv", delimiter=";", encoding="iso-8859-1", dtype={'title': str, 'genres': str,
                                                                                          'original_language': str,
                                                                                          'production_companies': str,
                                                                                          'budget': float,
                                                                                          'revenue': float,
                                                                                          'runtime': float,
                                                                                          'vote_average': float,
                                                                                          'vote_count': float,
                                                                                          'keywords': str},
                              parse_dates=['release_date'], dayfirst=True, on_bad_lines='skip')
        self.df = self.df[['title', 'genres', 'original_language', 'release_date', 'budget', 'revenue', 'runtime',
                           'vote_average', 'vote_count', 'keywords', 'production_companies', 'overview', 'status',
                           'tagline', 'popularity', 'credits']]
        self.total_size = len(self.df)
        self.df = self.df.drop_duplicates(subset=['title', 'release_date'])
        self.df['release_date'] = pd.to_datetime(self.df['release_date'], format='%d.%m.%Y', errors='coerce').dt.date

        # self.df.fillna('', inplace=True)
        self.df['keywords'].fillna('', inplace=True)
        self.df['genres'].fillna('', inplace=True)
        self.df['production_companies'].fillna('', inplace=True)
        self.df['status'].fillna('', inplace=True)
        self.df['credits'].fillna('', inplace=True)
        self.df['production_companies'] = self.df['production_companies'].str.replace('Metro-Goldwyn-Mayer',
                                                                                      'Metro Goldwyn Mayer')
        self.filtered_df = self.df.copy()

        # self.df['release_year'] = pd.DatetimeIndex(self.df['release_date']).year
        self.release_year = list(pd.DatetimeIndex(self.df['release_date']).year.unique())

        language_counts = self.filtered_df['original_language'].value_counts()
        self.languages = language_counts.index.tolist()
        self.languages.insert(0, "")

        self.genres = list(self.filtered_df['genres'].str.split('-').explode().unique())
        self.genres.sort()

        keyword_counts = self.filtered_df['keywords'].str.split('-').explode().value_counts()
        self.keywords = keyword_counts.index.tolist()
        self.original_keywords = list(self.filtered_df['keywords'].str.split('-').explode().unique())

        production_counts = self.filtered_df['production_companies'].str.split('-').explode().value_counts()
        self.original_production = list(self.filtered_df['production_companies'].str.split('-').explode().unique())
        self.productions = production_counts.index.tolist()

        actor_counts = self.filtered_df['credits'].str.split('-').explode().value_counts()
        self.original_actors = list(
            self.filtered_df['credits'].str.split('-').str.contains(' ').explode().unique())
        actors = actor_counts.index.tolist()
        self.real_actors = [actor for actor in actors if ' ' in actor]



    @property
    def size(self):
        return self.total_size

    @property
    def filtered_size(self):
        return len(self.filtered_df)


