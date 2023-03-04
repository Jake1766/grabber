import json

with open('books.json') as file:
    book_dict = json.loads(file.read())

for id in book_dict:
    print(book_dict[id]['title'])

print(f'titles found: {len(book_dict)}')

