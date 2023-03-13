import read_json

# need to reduce html to plain text
json_path = 'previous_outputs/all_books.json'


json_reader = read_json.Json_reader(json_path)

json_reader.extract_json()

dict = json_reader.book_dict

print(dict)
for item in dict:
    description = dict[item]['description']
    print(dict[item]['description'])

