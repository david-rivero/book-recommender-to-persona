import os
import requests
import time

from bs4 import BeautifulSoup
import pandas as pd


BASE_URL_GOODREADS = 'https://www.goodreads.com/book/show/{id}'
GOODREADS_DESC_SELECTOR = '.mainContentContainer #description span'
GOODREADS_GENRE_SELECTOR = ('.stacked .bigBoxContent '
    '.elementList .left .bookPageGenreLink')
GOODREADS_DATASET = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'base_dataset/books.csv')
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/56.0.2924.87 Safari/537.36')
}
CLIENT_ERROR_STATUS_CODE = 400 


def build_goodreads_data():
    books_dataset = pd.read_csv(GOODREADS_DATASET, error_bad_lines=False)
    description_column = []
    genres_column = []

    print('Initializing book data importing...')

    try:
        for ix, row in books_dataset.iterrows():
            book_id = row.get('bookID')
            print('Extracting book info from book id {book_id} ...'.format(
                book_id=book_id))

            book_detail = requests.get(
                BASE_URL_GOODREADS.format(id=book_id),
                headers=HEADERS)
            if book_detail.status_code < CLIENT_ERROR_STATUS_CODE:
                book_parsed = BeautifulSoup(book_detail.text, 'html.parser')

                # Extract description
                desc_selector = book_parsed.select(
                    GOODREADS_DESC_SELECTOR).pop()
                desc_text = desc_selector.text
                description_column.append(desc_text)

                # Extract genres related
                genres_selector = book_parsed.select(GOODREADS_GENRE_SELECTOR)
                genre_result = []
                for genre in genres_selector:
                    genre_result.append(genre.text)
                genres_column.append('::'.join(genre_result))

            print('Book info extracted!')
            time.sleep(2.5)
    except Exception:
        # TODO: Implement a better catching exception for bad requests
        pass

    print('Exporting information into CSV')

    # Creating columns
    books_dataset.loc[:, 'description'] = pd.Series(description_column)
    books_dataset.loc[:, 'genres'] = pd.Series(genres_column)

    # Exporting data
    csv_export_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'base_dataset/books_built.csv'
    )
    open(csv_export_path, 'w').close()
    books_dataset.to_csv(csv_export_path, index=False)

    print('Info exported')
