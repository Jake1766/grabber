import json
import time

path = 'books.json'

run = True

with open('books.json') as file:
    book_dict = json.loads(file.read())

for id in book_dict:
    print(book_dict[id]['title'])

print(f'titles found: {len(book_dict)}')

class Json_reader:
    #constructor method
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_json(self):
        with open('books.json') as file:
            book_dict = json.loads(file.read())

    def print_titles(self):
        for id in book_dict:
            print(book_dict[id]['title'])



json_reader = Json_reader(path)
book_dict = json_reader.extract_json()





