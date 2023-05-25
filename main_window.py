from tkinter import *
from tkinter.ttk import *

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

        movie_table_columns = ('name', 'genre', 'language', 'production', 'release_date', 'budget', 'revenue',
                               'runtime', 'vote_average', 'vote_count')
        self.movie_table = Treeview(self.search, columns=movie_table_columns, show='headings')
        self.movie_table.heading('name', text='Название')
        self.movie_table.heading('genre', text='Жанр')
        self.movie_table.heading('language', text='Язык оригинала')
        self.movie_table.heading('production', text='Кинокомпания')
        self.movie_table.heading('release_date', text='Дата выхода')
        self.movie_table.heading('budget', text='Бюджет')
        self.movie_table.heading('revenue', text='Выручка')
        self.movie_table.heading('runtime', text='Продолжительность')
        self.movie_table.heading('vote_average', text='Средняя оценка')
        self.movie_table.heading('vote_count', text='Кол-во оценок')
        self.movie_table.column('name', width=250)
        self.movie_table.column('genre', width=130)
        self.movie_table.column('language', width=100)
        self.movie_table.column('production', width=120)
        self.movie_table.column('release_date', width=80)
        self.movie_table.column('budget', width=90)
        self.movie_table.column('revenue', width=90)
        self.movie_table.column('runtime', width=100)
        self.movie_table.column('vote_average', width=95)
        self.movie_table.column('vote_count', width=90)
        self.movie_table.grid(row=0, column=1)

        """
        Название - текстовый ввод
        Жанр, Язык, Кинокомпания - выпадающий список
        Дата - диапазон дат
        Продолжительность - диапазон
        Средняя оценка - диапазон
        Кол-во оценок - диапазон
        Теги - текстовый ввод
        Актёры - ???
        Кнопка поиска
        """

        self.mainloop()
