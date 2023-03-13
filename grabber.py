# This will take the list of ids and output:
# title
# condition
# description with subsections
# links to hi res images

# error on 184168066720  - no title?
#  File "C:\Users\jaker\AppData\Roaming\Python\Python39\site-packages\selenium\webdriver\remote\webdriver.py", line 830, in find_element
#     return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
#   File "C:\Users\jaker\AppData\Roaming\Python\Python39\site-packages\selenium\webdriver\remote\webdriver.py", line 440, in execute
#     self.error_handler.check_response(response)
#   File "C:\Users\jaker\AppData\Roaming\Python\Python39\site-packages\selenium\webdriver\remote\errorhandler.py", line 245, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="vi-lkhdr-itmTitl"]"}


# TODO
#   - tidy print statements DONE
#   - update output with JSON on every loop DONE
#   - implement error catching for when value not found
#       - should retry 5 or so times
#       - should create list of failed books


# <<<IMPORTS>>>

# selenium:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# JSON
import json
# my json reader
import read_json

# array of ids
from id_array import id_array


driver = webdriver.Chrome('./chromedriver')

test_array = ['171570150605', '181925464719', '181952265161', '172087438233']

# exceptions
no_condition = ['173027969655']
no_title = ['184168066720']
no_image = ['174686231699']

# unknown (no title?) seems to work???
uk1 = ['184168072604']


# <<<SET ARRAY>>>
main_array = id_array


# <<<LOCATORS>>>
title_locator = 'vi-lkhdr-itmTitl'
condition_locator = 'ux-textspans--ITALIC'
description_locator = 'desc_ifr'
img_locator = 'ux-image-filmstrip-carousel-item'
active_image_locator = "ux-image-carousel-item active image"
price_locator = 'x-price-primary'
postage_locator = 'ux-labels-values--shipping'


#######################################################################################

# <<<CLASSES>>>


class Book:
    def __init__(self, page_id, title, condition, description, img_links, price, postage):
        self.page_id = page_id
        self.title = title
        self.condition = condition
        self.description = description
        self.img_links = img_links
        self.price = price
        self.postage = postage


class Jsonify:

    def write_to_file(self):
        # # converts dictionary to JSON
        # obj = json.dumps(grabber.books, indent=4)


        # writes JSON to file
        with open('books.json', 'w') as f:
            json.dump(grabber.books, f)
        print('\nwritten to file.')


class Grabber:
    # constructor method
    def __init__(self, id_array, driver):
        self.id_arrray = id_array
        self.driver = driver
        self.books = {}
        self.error_record = []
        self.current_id = '0'

    # <<<UTILITY FUNCTIONS>>>

    # loads url into driver
    def load_page(self, page_id):
        url = f'https://www.ebay.co.uk/itm/{page_id}?hash=item2a8c275483:g:6SEAAOSwVRpZmvjC&amdata=enc%3AAQAHAAAAoDBT52CV4ai8IlB2jaG%2F8u9IZUIx6BKYkZxarIILJSXJrH2x6F2FwqGxCG78%2B3ujWawxphu6KBBvkMd8nUX%2BFRzEBaFpdw%2BE2QgAKk5tKVtNyjLF35xzkhSwHLuevOAWFXQqM14lqqiZSNToA5wTIxfd5mF%2FOBnp0hWtQQ0kSKNdXASARyPKKKop6spGrayCDxtSlCFZKXYx2Db9OyQD%2BTo%3D%7Ctkp%3ABk9SR86p--7RYQ'
        driver = self.driver
        print('loading page for ' + str(page_id))
        print(f'url is:\n{url}')
        return driver.get(url)

    def grab_by_id(self, HTML_id):

        try:
            element = self.driver.find_element(By.ID, HTML_id)
            return element
        except NoSuchElementException:
            self.error_log(HTML_id)
            return 'failed'

    def grab_by_class(self, HTML_class):
        try:
            element = self.driver.find_element(By.CLASS_NAME, HTML_class)
            return element
        except NoSuchElementException:
            self.error_log(HTML_class)

    # grabs HTML from an element
    def grab_html(self, element):
        if element != 'failed':
            innerHTML = element.get_attribute('innerHTML')
            return innerHTML
        else:
            self.error_log(element)

    def grab_src(self, element):
        try:
            src = element.get_attribute('src')
            return src

        except:
            self.error_log(element)
            return 'failed'

    def error_log(self, item):
        error = f'Error: {item} not found on page: {self.current_id}\n'
        print(error)
        self.error_record.append(error)

        with open('error_log.txt', 'w') as file:
            file.write(str(self.error_record))




    # <<<METHODS>>>

    # grab title



    def grab_title(self):
        element = self.grab_by_id(title_locator)
        title = self.grab_html(element)
        print('\ntitle is:')
        print(title)
        return title

    # grab condition
    def grab_condition(self):
        try:
            element = self.grab_by_class(condition_locator)
            condition = self.grab_html(element)
            print('\ncondition is:')
            print(condition)
            return condition

        except:
            self.error_log(condition_locator)
            return 'failed'

    # grab description
    def grab_description(self):
        element = self.grab_by_id(description_locator)
        src = self.grab_src(element)
        print(f'\ndescription found')
        return src

    def grab_imgs(self):
        count = 0
        links = []
        try:
            img_links = driver.find_elements(By.CLASS_NAME, img_locator)

            #need to grab active image seperately
            active = driver.find_element(By.CSS_SELECTOR, "div.ux-image-carousel-item");
            img = active.find_element(By.TAG_NAME, 'img')
            link = img.get_attribute('src')
            links.append(link)

            for link in img_links:
                element = link.find_elements(By.TAG_NAME, 'img')
                src = element[count].get_attribute('src')
                links.append(src)
            links = self.img_process(links)
            print(f'\nimage links found')
            return links
        except:
            print('failed to find image')
            return 'failed'

    # grab price
    def grab_price(self):
        try:
            element = driver.find_element(By.CLASS_NAME, price_locator)
            final = element.find_element(By.CLASS_NAME, 'ux-textspans')
            price = final.get_attribute('innerHTML')
            price = price[1:]
            print(f'\nprice is:\n{price}')
            return str(price)

        except:
            self.error_log('price')
            return 'failed'

    def grab_postage(self):
        try:
            element = driver.find_element(By.CLASS_NAME, postage_locator)
            final = element.find_element(By.CLASS_NAME, 'ux-textspans--BOLD')
            postage = final.get_attribute('innerHTML')
            print(f'\npostage is:\n{postage}')
            return postage

        except:
            self.error_log('postage')
            return 'failed'

    def add_to_dict(self, new_book):
        print('\nnew_book.page_id:')
        print(new_book.page_id)
        obj = {
            'page_id': new_book.page_id,
            'title': new_book.title,
            'condition': new_book.condition,
            'description': new_book.description,
            'img_links': new_book.img_links,
            'price': new_book.price,
            'postage': new_book.postage
        }
        key = obj['page_id']
        self.books[key] = obj



    # <<<PROCESSORS>>

    # process image url to hi-res urls

    def img_process(self, array):
        processed_array = []
        for item in array:
            split_items = item.split('s-')
            url = split_items[0] + 's-l1600.jpg'
            # prevent multiple entries
            if url not in processed_array:
                processed_array.append(url)

        return processed_array


    # process all data to JSON

    # <<<MAIN LOOP>>>

    def run(self, array):
        count = 1
        driver = self.driver

        # iterates through all items in array
        for page_id in array:
            self.current_id = page_id
            print('\ngrabbing from ' + page_id + '\n')
            print(f'titles checked: {count}/{len(id_array)}')
            # calcs % progress, rounds to 2 dp
            print(f'progress:\n{round(count/len(id_array)*100, 2)}%')
            count += 1

            # loads page onto driver
            url = f'https://www.ebay.co.uk/itm/{page_id}?hash=item2a8c275483:g:6SEAAOSwVRpZmvjC&amdata=enc%3AAQAHAAAAoDBT52CV4ai8IlB2jaG%2F8u9IZUIx6BKYkZxarIILJSXJrH2x6F2FwqGxCG78%2B3ujWawxphu6KBBvkMd8nUX%2BFRzEBaFpdw%2BE2QgAKk5tKVtNyjLF35xzkhSwHLuevOAWFXQqM14lqqiZSNToA5wTIxfd5mF%2FOBnp0hWtQQ0kSKNdXASARyPKKKop6spGrayCDxtSlCFZKXYx2Db9OyQD%2BTo%3D%7Ctkp%3ABk9SR86p--7RYQ'

            print(f'\nurl is:\n{url}')

            driver.get(url)

            title = self.grab_title()
            condition = self.grab_condition()
            description = self.grab_description()
            img_links = self.grab_imgs()
            price = self.grab_price()
            postage = self.grab_postage()

            self.new_book = Book(page_id, title, condition, description, img_links, price, postage)
            self.add_to_dict(self.new_book)

            # writes current dict to file
            jsonify.write_to_file()

            # this prints all collected titles on each loop
            json_reader = read_json.Json_reader('books.json')
            json_reader.extract_json()
            json_reader.print_titles()





#######################################################################################

# initialise classes

grabber = Grabber(main_array, driver)
jsonify = Jsonify()


grabber.run(main_array)

