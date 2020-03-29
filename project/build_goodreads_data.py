import os
import requests

from bs4 import BeautifulSoup
import pandas as pd


BASE_URL_GOODREADS = 'https://www.goodreads.com/book/show/{id}'
GOODREADS_DESC_SELECTOR = '.mainContentContainer #description'
GOODREADS_GENRE_SELECTOR = ('.stacked .bigBoxContent '
    '.elementList .left .bookPageGenreLink')
GOODREADS_DATASET = 'base_dataset/books.csv'


def build_goodreads_data():
    books_dataset = pd.read_csv(GOODREADS_DATASET)
    description_column = []
    for row in books_dataset:
        book_id = row.get('bookID')
        book_detail = requests.get(BASE_URL_GOODREADS.format(id=book_id))
        book_parsed = BeautifulSoup(book_detail.text, 'html.parser')
        desc_selector = book_parsed.select(GOODREADS_DESC_SELECTOR)
        desc_text = desc_selector.get_text()
        description_column.append(desc_text)
    books_dataset['description'] = description_column
    books_dataset.to_csv('base_dataset/books_built.csv')
