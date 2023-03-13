import read_json

# need to reduce html to plain text
json_path = 'previous_outputs/all_books.json'


class Html_parse:
    def __init__(self):
        running = True

    def main_loop(self):
        while self.running:
            pass


# loads json from path and stores data in dictionary
json_reader = read_json.Json_reader(json_path)
json_reader.extract_json()
dict = json_reader.book_dict



for item in dict:
    description = dict[item]['description']
    print(description)

