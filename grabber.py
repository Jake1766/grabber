# This will take the list of ids and output:
# title
# condition
# description with subsections
# links to hi res images

# <<<IMPORTS>>>

# selenium:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# JSON
import json

# array of ids
from id_array import id_array

driver = webdriver.Chrome('./chromedriver')

test_array = ['171570150605', '181925464719', '181952265161', '172087438233']

# exceptions
no_condition = ['173027969655']


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
        print('\nwriting to file...\n')

        # # converts dictionary to JSON
        # obj = json.dumps(grabber.books, indent=4)

        # writes JSON to file
        with open('books.json', 'w') as f:
            json.dump(grabber.books, f)
        print('\nwritten to file.\n')



class Grabber:
    # constructor method
    def __init__(self, id_array, driver):
        self.id_arrray = id_array
        self.driver = driver
        self.books = {}

    # <<<UTILITY FUNCTIONS>>>

    # loads url into driver
    def load_page(self, page_id):
        driver = self.driver
        print('loading page for ' + str(page_id))
        return driver.get(f'https://www.ebay.co.uk/itm/{page_id}?hash=item2a8c275483:g:6SEAAOSwVRpZmvjC&amdata=enc%3AAQAHAAAAoDBT52CV4ai8IlB2jaG%2F8u9IZUIx6BKYkZx'
                   f'arIILJSXJrH2x6F2FwqGxCG78%2B3ujWawxphu6KBBvkMd8nUX%2BFRzEBaFpdw%2BE2QgAKk5tKVtNyjLF35xzkhSwHLuevOAWFXQqM14lqqiZSNToA5wTIxfd5mF%2FO'
                   f'Bnp0hWtQQ0kSKNdXASARyPKKKop6spGrayCDxtSlCFZKXYx2Db9OyQD%2BTo%3D%7Ctkp%3ABk9SR86p--7RYQ')

    def grab_by_id(self, HTML_id):
        driver = self.driver
        element = driver.find_element(By.ID, HTML_id)
        return element

    def grab_by_class(self, HTML_class):
        driver = self.driver
        try:
            element = driver.find_element(By.CLASS_NAME, HTML_class)
            return element
        except NoSuchElementException:
            return '<p1></p1>'

    # grabs HTML from an element
    def grab_html(self, element):
        innerHTML = element.get_attribute('innerHTML')
        return innerHTML

    def grab_src(self, element):
        src = element.get_attribute('src')
        return src

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
        element = self.grab_by_class(condition_locator)
        condition = self.grab_html(element)
        print('\ncondition is:')
        print(condition)
        return condition

    # grab description
    def grab_description(self):
        element = self.grab_by_id(description_locator)
        src = self.grab_src(element)
        print(f'\ndescription found at:\n{src}')
        return src

    def grab_imgs(self):
        count = 0
        links = []
        img_links = driver.find_elements(By.CLASS_NAME, img_locator)

        #need to grab active image seperately
        active = driver.find_element(By.CSS_SELECTOR, "div.ux-image-carousel-item");
        img = active.find_element(By.TAG_NAME, 'img')
        link = img.get_attribute('src')
        links.append(link)

        for link in img_links:
            element = link.find_elements(By.TAG_NAME, 'img')
            src = element[count].get_attribute('src')
            print(src)
            links.append(src)
        links = self.img_process(links)
        print(f'\nimage links: {links}')
        return links

    # grab price
    def grab_price(self):
        element = driver.find_element(By.CLASS_NAME, price_locator)
        final = element.find_element(By.CLASS_NAME, 'ux-textspans')
        price = final.get_attribute('innerHTML')
        price = price[1:]
        print(f'\nprice is:\n{price}')
        return str(price)

    def grab_postage(self):
        element = driver.find_element(By.CLASS_NAME, postage_locator)
        final = element.find_element(By.CLASS_NAME, 'ux-textspans--BOLD')
        postage = final.get_attribute('innerHTML')
        print(f'\npostage is:\n{postage}')
        return postage

    def add_to_dict(self, new_book):
        print('\nnew_book.page_id:\n')
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
        print('\nobj:\n')
        print(obj)
        key = obj['page_id']
        self.books[key] = obj



    # <<<PROCESSORS>>

    # process image url to hi-res urls

    def img_process(self, array):
        print(array)
        processed_array = []
        for item in array:
            split_items = item.split('s-')
            url = split_items[0] + 's-l1600.jpg'
            if url not in processed_array:
                processed_array.append(url)

        return processed_array


    # process all data to JSON



    # <<<MAIN LOOP>>>

    def run(self, array):
        count = 1
        driver = self.driver
        books = []

        # iterates through all items in array
        for page_id in array:
            print('\ngrabbing from ' + page_id)
            print(f'titles checked: {count}')
            count += 1

            # loads page onto driver
            driver.get(
                f'https://www.ebay.co.uk/itm/{page_id}?hash=item2a8c275483:'
                f'g:6SEAAOSwVRpZmvjC&amdata=enc%3AAQAHAAAAoDBT52CV4ai8IlB2j'
                f'aG%2F8u9IZUIx6BKYkZxarIILJSXJrH2x6F2FwqGxCG78%2B3ujWawxph'
                f'u6KBBvkMd8nUX%2BFRzEBaFpdw%2BE2QgAKk5tKVtNyjLF35xzkhSwHLu'
                f'evOAWFXQqM14lqqiZSNToA5wTIxfd5mF%2FOBnp0hWtQQ0kSKNdXASARy'
                f'PKKKop6spGrayCDxtSlCFZKXYx2Db9OyQD%2BTo%3D%7Ctkp%3ABk9SR86p--7RYQ')

            title = self.grab_title()
            condition = self.grab_condition()
            description = self.grab_description()
            img_links = self.grab_imgs()
            price = self.grab_price()
            postage = self.grab_postage()

            new_book = Book(page_id, title, condition, description, img_links, price, postage)
            self.add_to_dict(new_book)


        for book in books:
            print(book.title)
            print(book.img_links)
            jsonify.json_create(book)



#######################################################################################

# initialise classes

grabber = Grabber(test_array, driver)
jsonify = Jsonify()


grabber.run(no_condition)
jsonify.write_to_file()
print(grabber.books)
