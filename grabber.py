# This will take the list of ids and output:
# title
# condition
# description with subsections
# links to hi res images

# <<<IMPORTS>>>

# selenium:
from selenium import webdriver
from selenium.webdriver.common.by import By

# array of ids
from id_array import id_array

driver = webdriver.Chrome('./chromedriver')

test_array = ['171570150605', '181925464719', '181952265161', '172087438233']


# <<<LOCATORS>>>
title_locator = 'vi-lkhdr-itmTitl'
condition_locator = 'ux-textspans--ITALIC'
description_locator = 'desc_ifr'
img_locator = 'ux-image-filmstrip-carousel-item'


#######################################################################################

# class declaration

class Book:
    def __init__(self, title, condition, description, img_links):
        self.title = title
        self.condition = condition
        self.description = description
        self.img_links = img_links


class Grabber:
    # constructor method
    def __init__(self, id_array, driver):
        self.id_arrray = id_array
        self.driver = driver

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
        element = driver.find_element(By.CLASS_NAME, HTML_class)
        return element

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
        print(f'description found at:\n{src}')
        return src

    def grab_imgs(self):
        count = 0
        links = []
        img_links = driver.find_elements(By.CLASS_NAME, img_locator)
        for link in img_links:
            element = link.find_elements(By.TAG_NAME, 'img')
            src = element[count].get_attribute('src')
            print(src)
            links.append(src)
        return links

    # grab price

    # grab image links

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

            new_book = Book(title, condition, description, img_links)
            books.append(new_book)

        for book in books:
            print(book.title)
            print(book.img_links)








#######################################################################################

grabber = Grabber(test_array, driver)
grabber.run(test_array)