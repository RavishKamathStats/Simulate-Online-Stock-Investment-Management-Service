# IMPORT LIBRARIES
import json
import requests
import sys
import yfinance as yf

# Firebase Database URLs (Replace these URLs with your actual Firebase URLs)
DATABASE_URLS = {
    0: 'https://dsci551-2324b-default-rtdb.firebaseio.com/',
    1: 'https://dsci551-2nd-default-rtdb.firebaseio.com/'
}

## Define any global methods
# HERE
# string hash function
def hash_func(name):
    num_db = 0
    char_sum = 0
    # get total number of book from both database
    for db in DATABASE_URLS:
        get_json = requests.get(DATABASE_URLS[db] + '.json')
        json_object = (get_json.json())
        if json_object == None:
            pass
        else:
            num_db += len(json_object)

    for character in name:
        char_sum += ord(character)

    # get modulo
    modulo = char_sum % 2
    return modulo

def get_yahoo():
    ticker = yf.Ticker('GOOGL').info
    market_price = ticker['regularMarketPrice']
    previous_close_price = ticker['regularMarketPreviousClose']
    print('Ticker: GOOGL')
    print('Market Price:', market_price)
    print('Previous Close Price:', previous_close_price)

def add_book(book_id, book_json):
    # INPUT : book id and book json from command line
    # RETURN : status code after pyhton REST call to add book [response.status_code]
    # EXPECTED RETURN : 200

    # python3 template.py add_book 130 '{"author": "John Smith", "price": 100, "title": "no title", "year": 5}'
    input_data = book_json
    input_data = json.loads(book_json)
    author_name = input_data.get("author")
    database_id = hash_func(author_name)
    link = DATABASE_URLS[database_id] + str(book_aid) + '.json'
    requests.put(link, data=book_json)
    return book_id

def search_by_author(author_name):
    # INPUT: Name of the author
    # RETURN: JSON object having book_ids as keys and book information as value [book_json] published by that author  
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}
    # python3 template.py search_by_author "tom"
    dict_list = dict()

    for db in DATABASE_URLS:
        get_json = requests.get(DATABASE_URLS[db] + '.json')
        json_object = (get_json.json())
        if json_object == None:
            print('database ', db, ' doesnt contain any records')
        else:
            for key, value in json_object.items():
                if (str(value.get("author")) == author_name):
                    dict_list.update({key:value})
    return dict_list

def search_by_year(year):
    # INPUT: Year when the book published
    # RETURN: JSON object having book_ids as key and book information as value [book_json] published in that year
    # EXPECTED RETURN TYPE: {'102': {'author': ... , 'price': ..., 'title': ..., 'year': ...}, '104': {'author': , 'price': , 'title': , 'year': }}
    # python3 template.py search_by_year 5
    dict_list = dict()

    for db in DATABASE_URLS:
        get_json = requests.get(DATABASE_URLS[db] + '.json')
        json_object = (get_json.json())
        if json_object == None:
            print('database ', db, ' doesnt contain any records')
        else:
            for key, value in json_object.items():
                if (value.get("year") == year):
                    dict_list.update({key:value})
    return dict_list
