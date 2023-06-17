import tkinter as tk
from tkinter import BOTH, SOLID, HORIZONTAL
from tkinter.ttk import Notebook, Treeview, Combobox, Entry, Label

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from movies_list import MoviesList

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Movie Stat')
        self.geometry('1060x750')

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
        self.plot = self.figure.add_subplot(111)
        self.chart_button = tk.Button(self.chart, text="DRAW", command=self.select_chart)
        self.clear_button = tk.Button(self.chart, text="Очистить график", command=self.clear_chart)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.chart_frame)
        self.canvas.get_tk_widget().pack()

        # self.chart_options_x = {tuple(self.data.release_year): 'Годы выхода', tuple(self.data.languages): 'Языки оригинала', tuple(self.data.productions): 'Производственные компании', tuple(self.data.genres): 'Жанры',tuple(self.data.keywords): 'Теги', tuple(self.data.real_actors): 'Актёры'}
        self.chart_options_x = {'Годы выхода': ('release_date', tuple(self.data.release_year)),
                                'Языки оригинала': ('original_language', tuple(self.data.languages)),
                                'Производственные компании': ('production_companies', tuple(self.data.productions)),
                                'Жанры': ('genres', tuple(self.data.genres)),
                                'Теги': ('keywords', tuple(self.data.keywords)),
                                'Актёры': ('credits', tuple(self.data.real_actors))}
        self.chart_keys_x = list(self.chart_options_x.keys())
        # self.reversed_chart_options = {value: key for key, value in self.chart_options_x.items()}
        self.reversed_chart_options_1 = {value[0]: key for key, value in self.chart_options_x.items()}
        self.reversed_chart_options_2 = {value[1]: key for key, value in self.chart_options_x.items()}

        self.chart_combobox_x = Combobox(self.chart_frame, values=self.chart_keys_x)

        diagram_options = ['Линейный график', 'Точечный график', 'Столбчатая диаграмма', 'Круговая диаграмма']
        self.diagram_combobox = Combobox(self.chart_frame, values=diagram_options)
        # self.chart_frame.grid(row=0, column=0)
        # self.chart_button.grid(row=1, column=0)
        self.chart_frame.pack(anchor='n')
        self.chart_combobox_x.pack()
        self.chart_button.pack(anchor='s')
        self.clear_button.pack()
        self.diagram_combobox.pack()


        # --- SEARCH ---
        self.sorted_column = 'popularity'
        self.sort_direction = False
        self.movie_table_columns = ('title', 'genres', 'original_language', 'release_date', 'budget', 'revenue',
                                    'runtime', 'vote_average', 'vote_count')
        self.movie_table = Treeview(self.search, columns=self.movie_table_columns, show='headings')
        self.movie_table.heading('title', text='Название', command=lambda: self.sort_table('title', False))
        self.movie_table.heading('genres', text='Жанры', command=lambda: self.sort_table('genres', False))
        self.movie_table.heading('original_language', text='Язык оригинала',
                                 command=lambda: self.sort_table('original_language', False))
        self.movie_table.heading('release_date', text='Дата выхода', command=lambda: self.sort_table('release_date', False))
        self.movie_table.heading('budget', text='Бюджет', command=lambda: self.sort_table('budget', False))
        self.movie_table.heading('revenue', text='Выручка', command=lambda: self.sort_table('revenue', False))
        self.movie_table.heading('runtime', text='Продолжительность', command=lambda: self.sort_table('runtime', False))
        self.movie_table.heading('vote_average', text='Средняя оценка', command=lambda: self.sort_table('vote_average', False))
        self.movie_table.heading('vote_count', text='Кол-во оценок', command=lambda: self.sort_table('vote_count', False))
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

        self.movie_table.bind('<ButtonRelease-1>', self.show_movie_details)

        self.next_button = tk.Button(self.search, text="Следующие", command=self.next_rows)
        self.next_button.grid(row=1, column=2, sticky='w')
        self.prev_button = tk.Button(self.search, text="Предыдущие", command=self.prev_rows)
        self.prev_button.grid(row=1, column=0, sticky='e')
        self.rows_loaded_label = tk.Label(self.search, text="Загружено строк: 0/0")
        self.rows_loaded_label.grid(row=1, column=1, sticky='s')

        self.search_frame = tk.Frame(self.search, borderwidth=1, relief=SOLID, width=1000, height=1000)
        self.info_frame = tk.Frame(self.search, borderwidth=1, relief=SOLID, width=300, height=300)
        self.sort_frame = tk.Frame(self.search)



        self.genre_label = tk.Label(self.search_frame, text='Жанры')
        self.genre_combobox = Combobox(self.search_frame, values=self.data.genres, state="readonly")
        self.genre_combobox.bind("<<ComboboxSelected>>", self.add_genre)
        self.selected_genres = []

        self.name_label = tk.Label(self.search_frame, text='Название')
        self.name_entry = Entry(self.search_frame)
        self.name_entry.bind("<KeyRelease>", self.update_table)

        self.language_label = Label(self.search_frame, text='Язык')
        self.language_combobox = Combobox(self.search_frame, values=self.data.languages, state="readonly")
        self.language_combobox.bind("<<ComboboxSelected>>", self.update_table)

        self.production_label = Label(self.search_frame, text='Кинокомпании')
        self.production_combobox = Combobox(self.search_frame, values=self.data.productions)
        self.production_combobox.bind("<KeyRelease>", self.search_production)
        self.production_combobox.bind("<<ComboboxSelected>>", self.add_production)
        self.selected_productions = []

        self.keyword_label = Label(self.search_frame, text='Теги')
        self.keyword_combobox = Combobox(self.search_frame, values=self.data.keywords)
        self.keyword_combobox.bind("<KeyRelease>", self.search_keyword)
        self.keyword_combobox.bind("<<ComboboxSelected>>", self.add_keyword)
        self.selected_keywords = []

        self.actor_label = Label(self.search_frame, text='Актёры')
        self.actor_combobox = Combobox(self.search_frame, values=self.data.real_actors)
        self.actor_combobox.bind("<KeyRelease>", self.search_actor)
        self.actor_combobox.bind("<<ComboboxSelected>>", self.add_actor)
        self.selected_actors = []

        self.min_rating_label = Label(self.search_frame, text="Минимальный рейтинг:")
        self.min_rating_slider = tk.Scale(self.search_frame, from_=1, to=10, orient=HORIZONTAL, length=200,
                                          resolution=0.1)
        self.max_rating_label = Label(self.search_frame, text="Максимальный рейтинг:")
        self.max_rating_slider = tk.Scale(self.search_frame, from_=1, to=10, orient=HORIZONTAL, length=200,
                                          resolution=0.1)
        self.max_rating_slider.set(10)
        self.min_vote_count_label = Label(self.search_frame, text="Минимальное количество оценок:")
        self.min_vote_count_slider = tk.Scale(self.search_frame, from_=0, to=33262, orient=HORIZONTAL, length=200,
                                              resolution=10)
        self.max_vote_count_label = Label(self.search_frame, text="Максимальное количество оценок:")
        self.max_vote_count_slider = tk.Scale(self.search_frame, from_=0, to=33262, orient=HORIZONTAL, length=200,
                                              resolution=10)
        self.max_vote_count_slider.set(33262)
        self.min_runtime_label = Label(self.search_frame, text="Минимальная продолжительность:")
        self.min_runtime_slider = tk.Scale(self.search_frame, from_=0, to=600, orient=HORIZONTAL, length=200)
        self.max_runtime_label = Label(self.search_frame, text="Максимальная продолжительность:")
        self.max_runtime_slider = tk.Scale(self.search_frame, from_=0, to=600, orient=HORIZONTAL, length=200)
        self.max_runtime_slider.set(600)

        self.title_info_label = Label(self.info_frame, wraplength=400)
        self.genres_info_label = Label(self.info_frame, wraplength=400)
        self.language_info_label = Label(self.info_frame)
        self.overview_info_label = Label(self.info_frame, wraplength=400)
        self.production_info_label = Label(self.info_frame, wraplength=400)
        self.release_info_label = Label(self.info_frame)
        self.budget_info_label = Label(self.info_frame)
        self.revenue_info_label = Label(self.info_frame)
        self.runtime_info_label = Label(self.info_frame)
        self.status_info_label = Label(self.info_frame)
        self.tagline_info_label = Label(self.info_frame, wraplength=400)
        self.rating_info_label = Label(self.info_frame)
        self.vote_count_info_label = Label(self.info_frame)
        self.keywords_info_label = Label(self.info_frame, wraplength=400)
        self.actors_info_label = Label(self.info_frame, wraplength=400)

        self.item_label = Label(self.search_frame, text='Параметров загружено 0/15')
        self.item_count = 0

        # self.release_date_start_date_entry = DateEntry(self.search_frame)
        # self.release_date_finish_date_entry = DateEntry(self.search_frame)

        # self.search_button.pack(anchor=SE, side=BOTTOM)
        '''self.release_date_start_date_entry.grid(column=0, row=0)
        self.release_date_finish_date_entry.grid(column=1, row=0)'''
        self.max_vote_count_slider.grid(row=7, column=4, padx=5)
        self.max_vote_count_label.grid(row=6, column=4, padx=5)
        self.min_vote_count_slider.grid(row=5, column=4, padx=5)
        self.min_vote_count_label.grid(row=4, column=4, padx=5)
        self.max_rating_slider.grid(row=7, column=0)
        self.max_rating_label.grid(row=6, column=0)
        self.min_rating_slider.grid(row=5, column=0)
        self.min_rating_label.grid(row=4, column=0)
        self.max_runtime_slider.grid(row=7, column=5, padx=5)
        self.max_runtime_label.grid(row=6, column=5, padx=5)
        self.min_runtime_slider.grid(row=5, column=5, padx=5)
        self.min_runtime_label.grid(row=4, column=5, padx=5)
        self.actor_combobox.grid(row=3, column=5)
        self.actor_label.grid(row=2, column=5)
        self.keyword_combobox.grid(row=3, column=4)
        self.keyword_label.grid(row=2, column=4)
        self.production_combobox.grid(row=1, column=5)
        self.production_label.grid(row=0, column=5)
        self.language_combobox.grid(row=3, column=0)
        self.language_label.grid(row=2, column=0)
        self.genre_combobox.grid(row=1, column=4)
        self.genre_label.grid(row=0, column=4)
        self.name_entry.grid(row=1, column=0)
        self.name_label.grid(row=0, column=0, columnspan=3)

        self.title_info_label.grid_remove()
        self.genres_info_label.grid_remove()
        self.language_info_label.grid_remove()
        self.overview_info_label.grid_remove()
        self.production_info_label.grid_remove()
        self.release_info_label.grid_remove()
        self.budget_info_label.grid_remove()
        self.revenue_info_label.grid_remove()
        self.runtime_info_label.grid_remove()
        self.status_info_label.grid_remove()
        self.tagline_info_label.grid_remove()
        self.rating_info_label.grid_remove()
        self.vote_count_info_label.grid_remove()
        self.keywords_info_label.grid_remove()
        self.actors_info_label.grid_remove()

        self.search_frame.grid(row=2, column=0, sticky='wn', padx=15, pady=25, columnspan=2)
        self.sort_frame.grid(row=3, column=0, sticky='nw', padx=15, columnspan=2)
        self.info_frame.grid_remove()

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
            self.data.filtered_df = self.data.filtered_df[
                self.data.filtered_df['original_language'] == selected_language]

        self.data.filtered_df = self.data.filtered_df[(self.data.filtered_df['vote_count'] >= min_vote_count) & (
                self.data.filtered_df['vote_count'] <= max_vote_count)]
        self.data.filtered_df = self.data.filtered_df[(self.data.filtered_df['vote_average'] >= min_rating) & (
                self.data.filtered_df['vote_average'] <= max_rating)]
        self.data.filtered_df = self.data.filtered_df[
            self.data.filtered_df['title'].str.lower().str.contains(search_title)]
        for genre in self.selected_genres:
            self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['genres'].str.contains(genre)]
        for keyword in self.selected_keywords:
            self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['keywords'].str.contains(keyword, regex=False)]
        for production in self.selected_productions:
            self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['production_companies'].str.contains(production)]
        for actor in self.selected_actors:
            self.data.filtered_df = self.data.filtered_df[self.data.filtered_df['credits'].str.contains(actor)]
        self.item_label.config(
            text=f"Параметров загружено: {self.item_count}/15")
        self.rows_loaded = 0
        self.data.filtered_df.sort_values(by=self.sorted_column, ascending=self.sort_direction, inplace=True)
        self.update_table_display()

    def add_keyword(self, event):
        keyword = self.keyword_combobox.get()
        if keyword not in self.selected_keywords and self.item_count < 15:
            self.selected_keywords.append(keyword)
            self.item_label.grid(row=9, column=0, sticky='w', columnspan=3)
            keyword_frame = tk.Frame(self.search_frame)
            keyword_frame.grid(row=self.item_count // 3 + 10, column=self.item_count % 3, sticky='w', padx=5)
            keyword_label = Label(keyword_frame, text=keyword)
            keyword_label.pack(side="left")
            remove_button = tk.Button(keyword_frame, text="x",
                                      command=lambda: self.remove_item(keyword, keyword_frame, self.selected_keywords))
            remove_button.pack(side="left")
            self.item_count = self.item_count + 1
            self.update_table()

    def add_genre(self, event):
        genre = self.genre_combobox.get()
        if genre not in self.selected_genres and self.item_count < 15:
            self.selected_genres.append(genre)
            self.item_label.grid(row=9, column=0, sticky='w', columnspan=3)
            genre_frame = tk.Frame(self.search_frame)
            genre_frame.grid(row=self.item_count // 3 + 10, column=self.item_count % 3, sticky='w', padx=5)
            genre_label = Label(genre_frame, text=genre)
            genre_label.pack(side="left")
            remove_button = tk.Button(genre_frame, text="x",
                                      command=lambda: self.remove_item(genre, genre_frame, self.selected_genres))
            remove_button.pack(side="left")
            self.item_count = self.item_count + 1
            self.update_table()

    def add_production(self, event):
        production = self.production_combobox.get()
        if production not in self.selected_productions and self.item_count < 15:
            self.selected_productions.append(production)
            self.item_label.grid(row=9, column=0, sticky='w', columnspan=3)
            production_frame = tk.Frame(self.search_frame)
            production_frame.grid(row=self.item_count // 3 + 10, column=self.item_count % 3, sticky='w', padx=5)
            production_label = Label(production_frame, text=production)
            production_label.pack(side="left")
            remove_button = tk.Button(production_frame, text="x",
                                      command=lambda: self.remove_item(production, production_frame, self.selected_productions))
            remove_button.pack(side="left")
            self.item_count = self.item_count + 1
            self.update_table()

    def add_actor(self, event):
        actor = self.actor_combobox.get()
        if actor not in self.selected_actors and self.item_count < 15:
            self.selected_actors.append(actor)
            self.item_label.grid(row=9, column=0, sticky='w', columnspan=3)
            actor_frame = tk.Frame(self.search_frame)
            actor_frame.grid(row=self.item_count // 3 + 10, column=self.item_count % 3, sticky='w', padx=5)
            actor_label = Label(actor_frame, text=actor)
            actor_label.pack(side="left")
            remove_button = tk.Button(actor_frame, text="x",
                                      command=lambda: self.remove_item(actor, actor_frame, self.selected_actors))
            remove_button.pack(side="left")
            self.item_count = self.item_count + 1
            self.update_table()

    def remove_item(self, item, item_frame, selected_items):
        selected_items.remove(item)
        item_frame.grid_remove()
        self.item_count = self.item_count - 1
        if self.item_count == 0:
            self.item_label.grid_remove()
        self.update_table()

    def search_keyword(self, event):
        search_term = self.keyword_combobox.get().lower()
        if search_term == '':
            filtered_values = self.data.original_keywords
        else:
            filtered_values = [value for value in self.data.original_keywords if search_term in value]
        self.keyword_combobox['values'] = filtered_values

    def search_production(self, event):
        search_term = self.production_combobox.get().lower()
        if search_term == '':
            filtered_values = self.data.original_production
        else:
            filtered_values = [value for value in self.data.original_production if search_term in value.lower()]
        self.production_combobox['values'] = filtered_values

    def search_actor(self, event):
        search_term = self.actor_combobox.get().lower()
        if search_term == '':
            filtered_values = self.data.original_actors
        else:
            filtered_values = [value for value in self.data.original_actors if search_term in value]
        self.actor_combobox['values'] = filtered_values

    def show_movie_details(self, event):
        if self.movie_table.identify_row(event.y):
            selected_item = self.movie_table.focus()
            movie_data = self.movie_table.item(selected_item)
            movie_info = movie_data['values']
            self.info_frame.grid(row=2, column=2, sticky='e', padx=15, pady=25, rowspan=2)
            if movie_info[0] != '':
                self.title_info_label.config(text="Название: " + movie_info[0])
                self.title_info_label.grid(row=0, column=0, sticky='w')
            else:
                self.title_info_label.grid_remove()
            if movie_info[1] != '':
                self.genres_info_label.config(text="Жанры: " + movie_info[1].replace("-", ", "))
                self.genres_info_label.grid(row=7, column=0, sticky='w')
            else:
                self.genres_info_label.grid_remove()
            if movie_info[2] != '':
                self.language_info_label.config(text="Язык оригинала: " + movie_info[2])
                self.language_info_label.grid(row=3, column=0, sticky='w')
            else:
                self.language_info_label.grid_remove()
            if movie_info[11] != '':
                self.overview_info_label.config(text="Синопсис: \n" + movie_info[11])
                self.overview_info_label.grid(row=12, column=0, sticky='w')
            else:
                self.overview_info_label.grid_remove()
            if movie_info[10] != '':
                self.production_info_label.config(text="Производственные компании: \n" + movie_info[10].replace("-", ", "))
                self.production_info_label.grid(row=8, column=0, sticky='w')
            else:
                self.production_info_label.grid_remove()
            if movie_info[3] != '':
                self.release_info_label.config(text="Дата выхода: " + movie_info[3])
                self.release_info_label.grid(row=2, column=0, sticky='w')
            else:
                self.release_info_label.grid_remove()
            if movie_info[4] != 0.0:
                self.budget_info_label.config(text="Бюджет: " + movie_info[4])
                self.budget_info_label.grid(row=9, column=0, sticky='w')
            else:
                self.budget_info_label.grid_remove()
            if movie_info[5] != 0.0:
                self.revenue_info_label.config(text="Сборы: " + movie_info[5])
                self.revenue_info_label.grid(row=10, column=0, sticky='w')
            else:
                self.revenue_info_label.grid_remove()
            if movie_info[6] != '':
                self.runtime_info_label.config(text="Продолжительность: " + movie_info[6])
                self.runtime_info_label.grid(row=4, column=0, sticky='w')
            else:
                self.runtime_info_label.grid_remove()
            if movie_info[7] != '':
                self.rating_info_label.config(text="Рейтинг: " + movie_info[7])
                self.rating_info_label.grid(row=5, column=0, sticky='w')
            else:
                self.rating_info_label.grid_remove()
            if movie_info[8] != '':
                self.vote_count_info_label.config(text="Количество оценок: " + movie_info[8])
                self.vote_count_info_label.grid(row=6, column=0, sticky='w')
            else:
                self.vote_count_info_label.grid_remove()
            if movie_info[12] != '':
                self.status_info_label.config(text="Статус: " + movie_info[12])
                self.status_info_label.grid(row=11, column=0, sticky='w')
            else:
                self.status_info_label.grid_remove()
            if movie_info[13] != '':
                self.tagline_info_label.config(text="Слоган: " + movie_info[13])
                self.tagline_info_label.grid(row=1, column=0, sticky='w')
            else:
                self.tagline_info_label.grid_remove()
            if movie_info[9] != '':
                self.keywords_info_label.config(text="Теги: \n" + movie_info[9].replace("-", ", "))
                self.keywords_info_label.grid(row=13, column=0, sticky='w')
            else:
                self.keywords_info_label.grid_remove()
            if movie_info[14] != '':
                self.actors_info_label.config(text="Каст: \n" + movie_info[15].replace("-", ", "))
                self.actors_info_label.grid(row=14, column=0, sticky='w')
            else:
                self.actors_info_label.grid_remove()

    def update_table_display(self):
        self.movie_table.delete(*self.movie_table.get_children())
        rows_to_show = self.data.filtered_df[self.rows_loaded:self.rows_loaded + 10]



        for index, row in rows_to_show.iterrows():
            self.movie_table.insert("", index, values=list(row))

        self.rows_loaded_label.config(
            text=f"Загружено строк: {self.rows_loaded + 1}-{self.rows_loaded + len(rows_to_show)}/{self.data.filtered_size}")

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
        # if direction:
        #     self.movie_table.heading(column, text=column + ' ▲')
        # else:
        #     self.movie_table.heading(column, text=column + ' ▼')
        self.sorted_column = column
        self.sort_direction = direction
        self.rows_loaded = 0
        self.update_table_display()
        column_index = self.movie_table_columns.index(column)
        self.movie_table.heading(column_index, command=lambda: self.sort_table(column, not direction))

    # --- CHART ---
    def clear_chart(self):
        self.plot.clear()
        self.canvas.draw()
        self.toolbar.update()
    def draw_bar_chart(self):
        self.plot.clear()
        self.canvas.draw()
        self.toolbar.update()
        chart_option = self.chart_combobox_x.get()
        chart_columns = self.chart_options_x[chart_option][0]
        chart_values = self.chart_options_x[chart_option][1]
        chart_values = tuple(filter(None, chart_values))
        movies_count = self.data.df[chart_columns].str.extract(str(chart_values)).value_counts().sort_index().head(1)
        self.plot.bar(movies_count.index, movies_count.values)
        # self.plot.set_yscale('log')
        self.canvas.draw()

    '''
    def draw_plot_chart(self):
        self.plot.clear()
        self.canvas.draw()
        self.toolbar.update()
        chart_option = self.chart_combobox_x.get()
        chart_value = self.reversed_chart_options[chart_option]
        movies_count = self.data.df[chart_value].value_counts().sort_index()
        self.plot.plot(movies_count.index, movies_count.values)
        self.canvas.draw()
    
    def draw_scatter_chart(self):
        self.plot.clear()
        self.canvas.draw()
        self.toolbar.update()
        chart_option = self.chart_combobox.get()
        chart_value = self.reversed_chart_options[chart_option]
        movies_count = self.data.df[chart_value].value_counts().sort_index()
        self.plot.scatter(movies_count.index, movies_count.values)
        self.canvas.draw()


    def draw_pie_chart(self):
        self.plot.clear()
        self.canvas.draw()
        self.toolbar.update()
        chart_option = self.chart_combobox.get()
        chart_value = self.reversed_chart_options_1[chart_option]
        movies_count = self.data.df[chart_value].value_counts().sort_index()
        self.plot.pie(movies_count.index, movies_count.values, radius=0.5)
        self.canvas.draw()
    '''

    def select_chart(self):
        selected_chart = self.diagram_combobox.get()
        if selected_chart == 'Линейный график':
            self.draw_plot_chart()
        elif selected_chart == 'Точечный график':
            self.draw_scatter_chart()
        elif selected_chart == 'Столбчатая диаграмма':
            self.draw_bar_chart()
        elif selected_chart == 'Круговая диаграмма':
            self.draw_pie_chart()
