from tkinter import *
from tkinter.ttk import *

from tkcalendar import DateEntry

from movies_list import MoviesList

"""
    Идеи:
        1. По клику в строке фильма открывается расширенная информация о нём
"""


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title('Movie Stat')
        self.geometry('1200x700')

        self.notebook = Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        self.search = Frame(self.notebook)
        self.chart = Frame(self.notebook)
        self.search.pack(expand=True, fill=BOTH)
        self.chart.pack(expand=True, fill=BOTH)
        self.notebook.add(self.search, text='Поиск и фильтрация')
        self.notebook.add(self.chart, text='Графики')

        self.data = MoviesList()
        self.rows_loaded = 0

        self.movie_table_columns = ('title', 'genres', 'original_language', 'release_date', 'budget', 'revenue',
                               'runtime', 'vote_average', 'vote_count')
        self.movie_table = Treeview(self.search, columns=self.movie_table_columns, show='headings')
        self.movie_table.heading('title', text='Название', command=lambda: self.sort_table('title', False))
        self.movie_table.heading('genres', text='Жанр', command=lambda: self.sort_table('genres', False))
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

        self.next_button = Button(self.search, text="Следующие", command=self.next_rows)
        self.next_button.grid(row=1, column=2, sticky='w')
        self.prev_button = Button(self.search, text="Предыдущие", command=self.prev_rows)
        self.prev_button.grid(row=1, column=0, sticky='e')
        self.rows_loaded_label = Label(self.search, text="Загружено строк: 0/0")
        self.rows_loaded_label.grid(row=1, column=1, sticky='s')

        self.search_frame = Frame(self.search, borderwidth=1, relief=SOLID, width=300, height=300)

        self.search_button = Button(self.search_frame, text='Поиск')
        self.genre_label = Label(self.search_frame, text='Жанр')
        self.genre_combobox = Combobox(self.search_frame)
        self.name_label = Label(self.search_frame, text='Название')
        self.name_entry = Entry(self.search_frame)
        self.language_label = Label(self.search_frame, text='Язык')
        self.language_combobox = Combobox(self.search_frame)
        self.production_label = Label(self.search_frame, text='Кинокомпания')
        self.production_combobox = Combobox(self.search_frame)
        self.release_date_start_date_entry = DateEntry(self.search_frame)
        self.release_date_finish_date_entry = DateEntry(self.search_frame)

        self.search_button.pack(anchor=SE, side=BOTTOM)
        '''self.release_date_start_date_entry.grid(column=0, row=0)
        self.release_date_finish_date_entry.grid(column=1, row=0)'''
        self.production_combobox.pack(anchor=W, side=BOTTOM)
        self.production_label.pack(anchor=W, side=BOTTOM)
        self.language_combobox.pack(anchor=W, side=BOTTOM)
        self.language_label.pack(anchor=W, side=BOTTOM)
        self.genre_combobox.pack(anchor=W, side=BOTTOM)
        self.genre_label.pack(anchor=W, side=BOTTOM)
        self.name_entry.pack(anchor=W, side=BOTTOM)
        self.name_label.pack(anchor=W, side=BOTTOM)

        self.search_frame.grid(row=2, column=0, sticky='w', padx=15)

        self.update_table_display()
        self.mainloop()

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