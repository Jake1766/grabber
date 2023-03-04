import json

with open('books.json') as file:
    book_dict = json.loads(file.read())

for id in book_dict:
    print('\n')
    print(book_dict[id]['title'])

