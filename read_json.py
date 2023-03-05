import json
import time



input = 'books.json'
output = ''

run = True

# with open(input) as file:
#     book_dict = json.loads(file.read())
#
# for id in book_dict:
#     print(book_dict[id]['title'])
#
# print(f'titles found: {len(book_dict)}')

class Json_reader:
    #constructor method
    def __init__(self, file_path):
        self.file_path = file_path
        self.book_dict = {}

    def extract_json(self):
        print('extracting json...')
        with open(input) as file:
            self.book_dict = json.loads(file.read())

    def print_titles(self):
        print('printing titles...')
        for id in self.book_dict:
            print(self.book_dict[id]['title'])

json_reader = Json_reader(input)

book_dict = json_reader.extract_json()
json_reader = Json_reader(input)




