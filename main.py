from mongoengine import *
from models import *
import json
import configparser

config = configparser.ConfigParser()

config.read('config.ini')

mongodb_url = config.get('DATABASE', 'mongodb_url')
mongodb_uri = quote_plus(mongodb_url)  # Екрануємо спеціальні символи у URL


try:
    disconnect()  # Disconnect from any existing connections
    connect(db='hw_8', host=mongodb_url)
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

# Функція завантаження авторів
def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author_data in authors:
            author = Author(full_name=author_data['fullname'],
                            born_date=author_data['born_date'], 
                            born_location=author_data['born_location'], 
                            description=author_data['description'] )
            author.save()
    print("Authors loaded successfully!")

# Функція завантаження цитат
def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote_data in quotes:
            author_name = quote_data['author']
            author = Author.objects(full_name=author_name).first()
            quote = Quote(tags=quote_data['tags'], author=author, quote=quote_data['quote'])
            quote.save()
    print("Quotes loaded successfully!")

# load_authors('authors.json')
# load_quotes('quotes.json')


def search_quotes(query):
    command, value = query.split(':')

    if command == 'name':
        author = Author.objects(full_name=value).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print('Автор не знайдений.')
    elif command == 'tag':
        quotes = Quote.objects(tags=value)
        for quote in quotes:
            print(quote.quote)
    elif command == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.quote)
    else:
        print('Невідома команда.')

while True:
    query = input('Введіть команду (наприклад, name: Steve Martin): ')
    if query == 'exit':
        break
    search_quotes(query)

