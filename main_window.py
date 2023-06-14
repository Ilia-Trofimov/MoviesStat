import tkinter as tk
from tkinter import BOTH, SOLID, HORIZONTAL
from tkinter.ttk import Notebook, Treeview, Combobox, Entry, Label

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from movies_list import MoviesList

"""
    Идеи:
        1. По клику в строке фильма открывается расширенная информация о нём
"""


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Movie Stat')
        self.geometry('1100x700')

        self.notebook = Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        self.search = tk.Frame(self.notebook)
        self.chart = tk.Frame(self.notebook)
        self.search.pack(expand=True, fill=BOTH)
        self.chart.pack(expand=True, fill=BOTH)
        self.notebook.add(self.search, text='Поиск и фильтрация')
        self.notebook.add(self.chart, text='Графики')

        self.data = MoviesList()
        self.rows_loaded = 0

        # --- CHART ---

        self.chart_frame = tk.Frame(self.chart)
        self.figure = Figure(figsize=(3, 3), dpi=200)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.chart_button = tk.Button(self.chart, text="DRAW", command=self.draw_chart)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chart_frame)
        self.canvas.get_tk_widget().pack()
        #self.chart_frame.grid(row=0, column=0)
        #self.chart_button.grid(row=1, column=0)
        self.chart_frame.pack(anchor='n')
        self.chart_button.pack(anchor='s')


        # --- SEARCH ---
        self.movie_table_columns = ('title', 'genres', 'original_language', 'release_date', 'budget', 'revenue',
                                    'runtime', 'vote_average', 'vote_count')
        self.movie_table = Treeview(self.search, columns=self.movie_table_columns, show='headings')
        self.movie_table.heading('title', text='Название', command=lambda: self.sort_table('title', False))
        self.movie_table.heading('genres', text='Жанры', command=lambda: self.sort_table('genres', False))
        self.movie_table.heading('original_language', text='Язык оригинала', command=lambda: self.sort_table('original_language', False))
        self.movie_table.heading('release_date', text='Дата выхода')
        self.movie_table.heading('budget', text='Бюджет')
        self.movie_table.heading('revenue', text='Выручка')
        self.movie_table.heading('runtime', text='Продолжительность')
        self.movie_table.heading('vote_average', text='Средняя оценка')
        self.movie_table.heading('vote_count', text='Кол-во оценок')
        self.movie_table.column('title', width=250)
        self.movie_table.column('genres', width=130)
        self.movie_table.column('original_language', width=100)
        self.movie_table.column('release_date', width=80)
        self.movie_table.column('budget', width=90)
        self.movie_table.column('revenue', width=90)
        self.movie_table.column('runtime', width=100)
        self.movie_table.column('vote_average', width=95)
        self.movie_table.column('vote_count', width=90)
        self.movie_table.grid(row=0, column=0, columnspan=3, pady=5, padx=15)

        self.next_button = tk.Button(self.search, text="Следующие", command=self.next_rows)
        self.next_button.grid(row=1, column=2, sticky='w')
        self.prev_button = tk.Button(self.search, text="Предыдущие", command=self.prev_rows)
        self.prev_button.grid(row=1, column=0, sticky='e')
        self.rows_loaded_label = tk.Label(self.search, text="Загружено строк: 0/0")
        self.rows_loaded_label.grid(row=1, column=1, sticky='s')

        self.search_frame = tk.Frame(self.search, borderwidth=1, relief=SOLID, width=1000, height=1000)

        language_counts = self.data.filtered_df['original_language'].value_counts()
        languages = language_counts.index.tolist()
        languages.insert(0, "")
        genre_counts = self.data.filtered_df['genres'].str.split('-').explode().value_counts()
        genres = genre_counts.index.tolist()
        keyword_counts = self.data.filtered_df['keywords'].str.split('-').explode().value_counts()
        keywords = keyword_counts.index.tolist()
        production_counts = self.data.filtered_df['production_companies'].str.split('-').explode().value_counts()
        productions = production_counts.index.tolist()

        # self.search_button = Button(self.search_frame, text='Поиск')
        self.genre_label = tk.Label(self.search_frame, text='Жанры')
        self.genre_combobox = Combobox(self.search_frame, values=genres)
        self.name_label = tk.Label(self.search_frame, text='Название')
        self.name_entry = Entry(self.search_frame)
        self.name_entry.bind("<KeyRelease>", self.update_table)
        self.language_label = Label(self.search_frame, text='Язык')
        self.language_combobox = Combobox(self.search_frame, values=languages)
        self.language_combobox.bind("<<ComboboxSelected>>", self.update_table)
        self.production_label = Label(self.search_frame, text='Кинокомпании')
        self.production_combobox = Combobox(self.search_frame, values=productions)
        self.keyword_label = Label(self.search_frame, text='Теги')
        self.keyword_combobox = Combobox(self.search_frame, values=keywords)
        self.min_rating_label = Label(self.search_frame, text="Минимальный рейтинг:")
        self.min_rating_slider = tk.Scale(self.search_frame, from_=1, to=10, orient=HORIZONTAL, length=200)
        self.max_rating_label = Label(self.search_frame, text="Максимальный рейтинг:")
        self.max_rating_slider = tk.Scale(self.search_frame, from_=1, to=10, orient=HORIZONTAL, length=200)
        self.max_rating_slider.set(10)
        self.min_vote_count_label = Label(self.search_frame, text="Минимальное количество оценок:")
        self.min_vote_count_slider = tk.Scale(self.search_frame, from_=0, to=33262, orient=HORIZONTAL, length=200)
        self.max_vote_count_label = Label(self.search_frame, text="Максимальное количество оценок:")
        self.max_vote_count_slider = tk.Scale(self.search_frame, from_=0, to=33262, orient=HORIZONTAL, length=200)
        self.max_vote_count_slider.set(33262)
        self.min_runtime_label = Label(self.search_frame, text="Минимальная продолжительность:")
        self.min_runtime_slider = tk.Scale(self.search_frame, from_=0, to=600, orient=HORIZONTAL, length=200)
        self.max_runtime_label = Label(self.search_frame, text="Максимальная продолжительность:")
        self.max_runtime_slider = tk.Scale(self.search_frame, from_=0, to=600, orient=HORIZONTAL, length=200)
        self.max_runtime_slider.set(600)

        # self.release_date_start_date_entry = DateEntry(self.search_frame)
        # self.release_date_finish_date_entry = DateEntry(self.search_frame)

        # self.search_button.pack(anchor=SE, side=BOTTOM)
        '''self.release_date_start_date_entry.grid(column=0, row=0)
        self.release_date_finish_date_entry.grid(column=1, row=0)'''
        self.max_vote_count_slider.grid(row=7, column=1, padx=15)
        self.max_vote_count_label.grid(row=6, column=1, padx=15)
        self.min_vote_count_slider.grid(row=5, column=1, padx=15)
        self.min_vote_count_label.grid(row=4, column=1, padx=15)
        self.max_rating_slider.grid(row=7, column=0)
        self.max_rating_label.grid(row=6, column=0)
        self.min_rating_slider.grid(row=5, column=0)
        self.min_rating_label.grid(row=4, column=0)
        self.max_runtime_slider.grid(row=7, column=2, padx=15)
        self.max_runtime_label.grid(row=6, column=2, padx=15)
        self.min_runtime_slider.grid(row=5, column=2, padx=15)
        self.min_runtime_label.grid(row=4, column=2, padx=15)
        self.keyword_combobox.grid(row=3, column=1)
        self.keyword_label.grid(row=2, column=1)
        self.production_combobox.grid(row=1, column=2)
        self.production_label.grid(row=0, column=2)
        self.language_combobox.grid(row=3, column=0)
        self.language_label.grid(row=2, column=0)
        self.genre_combobox.grid(row=1, column=1)
        self.genre_label.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=0)
        self.name_label.grid(row=0, column=0)

        self.search_frame.grid(row=2, column=0, sticky='w', padx=15, pady=25, columnspan=2)

        self.min_rating_slider.bind("<B1-Motion>", self.update_table)
        self.max_rating_slider.bind("<B1-Motion>", self.update_table)
        self.min_vote_count_slider.bind("<B1-Motion>", self.update_table)
        self.max_vote_count_slider.bind("<B1-Motion>", self.update_table)
        self.min_runtime_slider.bind("<B1-Motion>", self.update_table)
        self.max_runtime_slider.bind("<B1-Motion>", self.update_table)

        self.update_table_display()
        self.mainloop()

    def update_table(self, event=None):
        selected_language = self.language_combobox.get()
        min_vote_count = self.min_vote_count_slider.get()
        max_vote_count = self.max_vote_count_slider.get()
        min_rating = self.min_rating_slider.get()
        max_rating = self.max_rating_slider.get()
        search_title = self.name_entry.get().lower()

        self.data.filtered_df = self.data.df

        if selected_language != "":
            self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['original_language'] == selected_language]

        self.data.filtered_df = self.data.filtered_df[(self.data.filtered_df['vote_count'] >= min_vote_count) & (self.data.filtered_df['vote_count'] <= max_vote_count)]
        self.data.filtered_df = self.data.filtered_df[(self.data.filtered_df['vote_average'] >= min_rating) & (self.data.filtered_df['vote_average'] <= max_rating)]
        self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['title'].str.lower().str.contains(search_title)]
        self.rows_loaded = 0
        self.update_table_display()

    def vote_count_update(self, event):
        min_vote_count = self.min_vote_count_slider.get()
        max_vote_count = self.max_vote_count_slider.get()
        self.data.filtered_df = self.data.df[
            (self.data.df['vote_count'] >= min_vote_count) & (
                    self.data.df['vote_count'] <= max_vote_count)]
        self.update_table_display()

    def rating_update(self, event):
        min_rating = self.min_rating_slider.get()
        max_rating = self.max_rating_slider.get()
        self.data.filtered_df = self.data.df[
            (self.data.df['vote_average'] >= min_rating) & (self.data.df['vote_average'] <= max_rating)]
        self.update_table_display()

    def title_update(self, event):
        search_title = self.name_entry.get().lower()
        self.data.filtered_df = self.data.df[
            self.data.df['title'].str.contains(search_title)]
        self.update_table_display()

    def language_update(self, event):
        selected_language = self.language_combobox.get()
        if selected_language != "":
            self.data.filtered_df = self.data.df[self.data.df['original_language'] == selected_language]
        self.update_table_display()

    def update_table_display(self):
        self.movie_table.delete(*self.movie_table.get_children())
        rows_to_show = self.data.filtered_df[self.rows_loaded:self.rows_loaded + 10]

        for index, row in rows_to_show.iterrows():
            self.movie_table.insert("", index, values=list(row))


        self.rows_loaded_label.config(
            text=f"Загружено строк: {self.rows_loaded + 1}-{self.rows_loaded + len(rows_to_show)}/{self.data.filtered_size}")

        '''
        if current_sort_column:
            sort_indicator = " ▲" if current_sort_order == "asc" else " ▼"
            table.heading(current_sort_column, text=current_sort_column + sort_indicator)
        '''

    def next_rows(self):
        self.rows_loaded += 10
        if self.rows_loaded >= self.data.filtered_size:
            self.rows_loaded = self.data.filtered_size - 10
        self.update_table_display()

    def prev_rows(self):
        if self.rows_loaded - 10 >= 0:
            self.rows_loaded -= 10
        self.update_table_display()

    def sort_table(self, column, direction):
        self.data.filtered_df.sort_values(by=column, ascending=direction, inplace=True)
        self.rows_loaded = 0
        self.update_table_display()
        self.movie_table.heading(self.movie_table_columns.index(column), command=lambda: self.sort_table(column, not direction))

    # --- CHART ---
    def draw_chart(self):
        plot = self.figure.add_subplot(111)
        plot.plot([[0,75], [3,44], [10,36]])
        self.canvas.draw()
        self.toolbar.update()