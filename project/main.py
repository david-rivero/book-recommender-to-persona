import pandas as pd

from .build_goodreads_data import build_goodreads_data
from .trainer import TrainerTemplate

if __name__ == '__main__':
    mtbi_model = TrainerTemplate()

    mtbi_df = pd.read_csv('base_dataset/mtbi.csv')
    mtbi_model.train_model(mtbi_df, 'type')

    build_goodreads_data()
    books_df = pd.read_csv('base_dataset/books_built.csv')
    book_personality_match = []
    for row in books_df:
        book_personality = mtbi_model.predict(row)
        book_personality_match.append(book_personality)
    books_df['Personality type'] = book_personality_match
    books_df.to_csv('base_dataset/book_personality_match.csv')

