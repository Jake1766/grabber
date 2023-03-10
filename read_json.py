import json
import time

class Json_reader:
    #constructor method
    def __init__(self, file_path):
        self.file_path = file_path
        self.book_dict = {}
        self.running = True
        self.menu_options = '1. Print all titles\n2. Print total price\nx: Exit\n: '


    def extract_json(self):
        print('extracting json...')
        with open(self.file_path) as file:
            print(f'extracting from {input}')
            self.book_dict = json.loads(file.read())

    def print_titles(self):
        print('\nprinting titles...\n')
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

    def main_loop(self):
        while self.running:
            self.main_options()


json_reader = Json_reader('previous_outputs/all_books.json')
json_reader.main_loop()


json_reader.extract_json()





