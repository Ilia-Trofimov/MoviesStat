import pandas as pd
import tkinter as tk
from tkinter import ttk

df = pd.read_csv("movies1.csv", delimiter=";", encoding="iso-8859-1", dtype={'title': str, 'genres': str,
                                                                             'original_language': str,
                                                                             'budget': float, 'revenue': float,
                                                                             'runtime': float, 'vote_average': float,
                                                                             'vote_count': float},
                 parse_dates=['release_date'], dayfirst=True, on_bad_lines='skip')
df = df[['title', 'genres', 'original_language', 'release_date', 'budget', 'revenue', 'runtime',
         'vote_average', 'vote_count']].rename(columns={"title": "Название", "genres": "Жанры",
                                                        "original_language": "Язык оригинала",
                                                        "release_date": "Дата выхода",
                                                        "budget": "Бюджет",
                                                        "revenue": "Сборы",
                                                        "runtime": "Продолжительность",
                                                        "vote_average": "Рейтинг",
                                                        "vote_count": "Количество оценок"})
df = df.drop_duplicates(subset=['Название', 'Дата выхода'])

df['Дата выхода'] = pd.to_datetime(df['Дата выхода'], format='%d.%m.%Y', errors='coerce')
df['Дата выхода'] = df['Дата выхода'].dt.date
df['Жанры'].fillna('', inplace=True)
filtered_df = df.copy()


def update_table(event=None):
    selected_language = language_var.get()
    min_rating = min_rating_slider.get()
    max_rating = max_rating_slider.get()
    min_vote_count = min_vote_count_slider.get()
    max_vote_count = max_vote_count_slider.get()

    global filtered_df, rows_loaded

    filtered_df = df.copy()
    if selected_language != "":
        filtered_df = filtered_df[filtered_df["Язык оригинала"] == selected_language]
    filtered_df = filtered_df[
        (filtered_df["Рейтинг"] >= min_rating) & (filtered_df["Рейтинг"] <= max_rating)
    ]
    filtered_df = filtered_df[
        (filtered_df["Количество оценок"] >= min_vote_count) & (filtered_df["Количество оценок"] <= max_vote_count)
    ]

    for genre in selected_genres:
        filtered_df = filtered_df[filtered_df['Жанры'].str.contains(genre)]
    rows_loaded = 0
    update_table_display()


def upload_table():
    global filtered_df, total_rows, rows_loaded

    filtered_df = df.copy()
    total_rows = len(filtered_df)
    rows_loaded = 0

    update_table_display()
    for column in df.columns:
        table.heading(column, text=column, command=lambda c=column: sort_table(c))


def update_table_display():
    table.delete(*table.get_children())
    rows_to_show = filtered_df[rows_loaded:rows_loaded + 10]
    total_rows = len(filtered_df)

    for index, row in rows_to_show.iterrows():
        table.insert("", index, values=list(row))

    rows_loaded_label.config(text=f"Загружено строк: {rows_loaded + 1}-{rows_loaded + len(rows_to_show)}/{total_rows}")
    for column in table["columns"]:
        table.heading(column, text=column)

    if current_sort_column:
        sort_indicator = " ▲" if current_sort_order == "asc" else " ▼"
        table.heading(current_sort_column, text=current_sort_column + sort_indicator)


def next_rows():
    global rows_loaded
    total_rows = len(filtered_df)
    rows_loaded += 10
    if rows_loaded >= total_rows:
        rows_loaded = total_rows - 10
    if rows_loaded < 0:
        rows_loaded = 0

    update_table_display()


def prev_rows():
    global rows_loaded
    rows_loaded -= 10
    if rows_loaded < 0:
        rows_loaded = 0

    update_table_display()


def sort_table(column):
    global current_sort_column, current_sort_order
    if current_sort_column == column:
        current_sort_order = "asc" if current_sort_order == "desc" else "desc"
    else:
        current_sort_column = column
        current_sort_order = "asc"

    filtered_df.sort_values(by=column, ascending=(current_sort_order == "asc"), inplace=True)
    update_table_display()


def add_genre(event):
    genre = genre_combobox.get()
    if genre not in selected_genres:
        selected_genres.append(genre)
        genre_label = tk.Label(root, text=genre)
        genre_label.pack(side="left", padx=5)
        remove_button = tk.Button(root, text="x", command=lambda: remove_genre(genre, genre_label, remove_button))
        remove_button.pack(side="left", padx=5)
        update_table()


def remove_genre(genre, genre_label, remove_button):
    selected_genres.remove(genre)
    genre_label.pack_forget()
    remove_button.pack_forget()
    update_table()


root = tk.Tk()

table = ttk.Treeview(root, show='headings')
table["columns"] = list(df.columns)

for column in df.columns:
    table.heading(column, text=column)

current_sort_column = ""
current_sort_order = ""

language_counts = df["Язык оригинала"].value_counts()

languages = language_counts.index.tolist()

languages.insert(0, "")

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, values=languages)

language_combobox.bind("<<ComboboxSelected>>", update_table)

min_rating_label = tk.Label(root, text="Минимальный рейтинг:")
min_rating_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, length=200, resolution=0.1)

max_rating_label = tk.Label(root, text="Максимальный рейтинг:")
max_rating_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, length=200, resolution=0.1)
max_rating_slider.set(10)

min_vote_count_label = tk.Label(root, text="Минимальное количество оценок:")
min_vote_count_slider = tk.Scale(root, from_=df['Количество оценок'].min(), to=df['Количество оценок'].max(),
                                orient=tk.HORIZONTAL, length=200, resolution=10)

max_vote_count_label = tk.Label(root, text="Максимальное количество оценок:")
max_vote_count_slider = tk.Scale(root, from_=df['Количество оценок'].min(), to=df['Количество оценок'].max(),
                                orient=tk.HORIZONTAL, length=200, resolution=10)
max_vote_count_slider.set(df['Количество оценок'].max())

min_rating_slider.bind("<B1-Motion>", update_table)
max_rating_slider.bind("<B1-Motion>", update_table)
min_vote_count_slider.bind("<B1-Motion>", update_table)
max_vote_count_slider.bind("<B1-Motion>", update_table)

rows_loaded_label = tk.Label(root, text="Загружено строк: 0/0")
rows_loaded_label.pack()

next_button = tk.Button(root, text="Следующие", command=next_rows)
next_button.pack()

prev_button = tk.Button(root, text="Предыдущие", command=prev_rows)
prev_button.pack()

genre_frame = tk.Frame(root)
genre_frame.pack()

genre_label = tk.Label(genre_frame, text="Жанры:")
genre_label.pack(side="left", padx=5)

selected_genres = []

genre_combobox = ttk.Combobox(root, values=list(df['Жанры'].str.split('-').explode().unique()), state="readonly")
genre_combobox.pack()
genre_combobox.bind("<<ComboboxSelected>>", add_genre)

table.pack()
language_combobox.pack()
min_rating_label.pack()
min_rating_slider.pack()
max_rating_label.pack()
max_rating_slider.pack()
min_vote_count_label.pack()
min_vote_count_slider.pack()
max_vote_count_label.pack()
max_vote_count_slider.pack()

upload_table()

root.mainloop()
