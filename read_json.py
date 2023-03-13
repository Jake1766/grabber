import json
import time

json_path = 'previous_outputs/all_books.json'
error_path = 'error_log.txt'


class Json_reader:
    #constructor method
    def __init__(self, file_path):
        self.file_path = file_path
        self.book_dict = {}
        self.running = True
        self.menu_options = '1. Print all titles\n2. Print total price\n3. View errors\nx: Exit\n: '

    # extracts json to dictionary
    def extract_json(self):
        print('extracting json...')
        with open(self.file_path) as file:
            print(f'extracting from {input}')
            self.book_dict = json.loads(file.read())

    def print_titles(self):
        print('\nprinting titles...\n')
        print(len(self.book_dict))
        for id in self.book_dict:
            print(self.book_dict[id]['title'])

    def price_total(self):
        total = 0
        for item in self.book_dict:
            price = self.book_dict[item]['price']
            print(price)
            print(total)
            price = price.replace(',', '')
            if price != 'failed':
                total += float(price)
            elif price == 'failed':
                print('invalid target...')

    def main_options(self):
        choice = input(self.menu_options)
        if choice == 'x':
            self.running = False
        if choice == 1:
            print('Printing titles...')
        if choice == 2:
            print('calculating total price')
        if choice == 3:
            error_reader = Error_reader(error_path)
            error_reader.main()

    def main_loop(self):
        while self.running:
            self.main_options()

class Error_reader:
    def __init__(self, file_path):
        self.file_path = file_path







