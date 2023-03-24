from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pyperclip
import read_json
import traceback
import os

import requests


import time

json_path = 'previous_outputs/all_books.json'
url = 'https://yeetskeetdelete-8142.myshopify.com/admin/products/new'
email = 'jakerandall07022@gmail.com'
# locators

title_locator = 'PolarisTextField1' # id
# description_pull_locator =
description_push_locator = 'product-description' # id name
img_locator = ''
price_locator = ''

# driver = webdriver.Chrome('./chromedriver')
# driver_2 = webdriver.Chrome('./chromedriver')


class Pusher:
    def __init__(self, dict):
        self.running = True
        self.driver = interface.driver
        self.driver_2 = interface.driver_2
        self.dict = dict

    # utility

    def enter(self, element):
        print('pressing enter...\n')
        element.send_keys(Keys.ENTER)

    def push_title(self, title):
        print(f'pushing title:\n{title}\n')
        element = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/input')
        element.send_keys(title)
        time.sleep(3)

    def push_description(self, desc_url):
        print(f'pushing description from {desc_url}\n')
        self.driver_2.get(desc_url)
        desc_html = self.driver_2.find_element(By.TAG_NAME, 'table')
        desc_html = desc_html.get_attribute('innerHTML')
        print(type(desc_html))
        print(f'\nhtml is:\n{desc_html}\n')

        # need to press button to write html
        html_button = self.driver.find_element(By.CSS_SELECTOR, "button.edsvs.mQNNA.B1Gi5")
        html_button.click()
        time.sleep(2)

        # should be able to input raw html now

        desc_box = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/div")
        desc_box.click()
        print('clicked description box...\n')
        pyperclip.copy(desc_html)
        desc_box.send_keys(Keys.CONTROL, 'v')
        print('description added.\n')

    def push_imgs(self, array):
        print(f'urls:\n{array}')
        for url in array:
            # need to press button to open entry field for url
            print(f'adding url: {url}\n')
            tries = 0

            while tries < 5:
                try:
                    print('attempting to click \'add url\' button...')
                    url_add_button = self.driver.find_element(By.CLASS_NAME, 'Polaris-Link_yj5sy')
                    url_add_button.click()
                    print('\nsuccess!\n')
                    tries = 5

                except:
                    print(f'failed to click \'add from url\' button x{tries}')
                    tries += 1

            tries = 0
            while tries < 5:
                try:
                    entry_field = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[2]/div/section/div/div/div/div[2]/div/div/input')
                    entry_field.click()
                    print('\nentry field select success!\n')
                    tries += 5

                except Exception as e:
                    print(f'failed to select entry field x{tries}')
                    print(f'\n{e}\n')
                    print(f'{traceback.format_exc()}\n')
                    tries += 1

            tries = 0
            while tries < 5:
                try:
                    entry_field.send_keys(url)
                    print('\nkey send success!\n')
                    tries = 5
                except:
                    print(f'failed to enter url x{tries}\n')
                    tries += 1

            tries = 0
            while tries < 5:
                try:
                    print('clicking url add button...')
                    submit_url = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[3]/div/div/div[2]/button[2]')
                    submit_url.click()
                    tries = 5
                except Exception as e:
                    tries += 1
                    print(f'\nadd url button click attempt x{tries}\n')
                    print(f'{traceback.format_exc}')
                    print(f'\n{e}\n')





    def push_imgs_2(self, urls):
        for link in urls:
            img_data = requests.get(link).content
            file_path = fr'C:\Users\jaker\Desktop\Migration\temp_images\temp_image_{urls.index(link)}.jpg'

            with open(file_path, 'wb') as handler:
                handler.write(img_data)

        for filename in os.listdir('temp_images'):
            file_path = fr'C:\Users\jaker\Desktop\Migration\temp_images/{filename}'
            print(f'\nfilepath is: {file_path}\n')
            print(f'filename is: {filename}\n')

            tries = 0
            while tries < 5:
                try:
                    print('attempting to click \'add img\' button...')

                    self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[2]/div/div/div[3]/div/div/div[2]/span/input').send_keys(file_path)

                    time.sleep(5)
                    print('\nsuccess??\n')
                    os.remove(file_path)
                    tries = 5

                except Exception as e:
                    print(f'failed to add image x{tries}')
                    print(f'\n{e}\n')
                    print(f'{traceback.format_exc}\n')
                    tries += 1




    def push_price(self, price):
        print('pushing price...\n')
        tries = 0
        while tries < 5:
            try:
                price_box = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div')
                price_box.click()
                print('\nsuccess!')
                tries = 5
            except:
                print('failed to click price box')
                tries += 1

        tries = 0
        while tries < 5:
            try:
                price_box = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div/input')
                price_box.send_keys(price)
                print('\nsuccess!\n')
                tries = 5

            except:
                print('failed to push price')
                tries += 1

    def save(self):
        print('saving product...')
        tries = 0
        while tries < 5:
            try:
                save_button = self.driver.find_element(By.CSS_SELECTOR, 'button.Polaris-Button_r99lw.Polaris-Button--primary_7k9zs')
                save_button.click()
                print('\nsuccess!\n')
                tries = 5

            except:
                print('attempted to save, ')

    def product_list_screen(self):
        print('navigating to product list screen\n')
        tries = 0
        while tries < 5:
            try:
                nav_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[1]/div/div/div[1]/div/nav/a')
                nav_button.click()
                print('\nsuccess!\n')
                tries = 5
            except:
                print(f'attempted to navigate to product list screen... x{tries}')
                tries += 1

    def new_product(self):
        print('adding new product...\n')
        tries = 0
        while tries < 5:
            try:
                new_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[1]/div/div/div[2]/div[2]/div/a')
                new_button.click()
                print('\nsuccess!\n')
                tries = 5

            except:
                print(f'attempted to navigate to new product... x{tries}')
                tries += 1


    def main(self):

        input('press enter to start')

        dict = self.dict

        for item in dict:

            book = dict[item]

            print(f'id is: {item}')

            try:
                self.push_title(book['title'])

            except Exception as e:
                print(e)

            try:
                self.push_description(book['description'])

            except Exception as e:
                print(e)

            try:
                self.push_imgs_2(book['img_links'])

            except Exception as e:
                print(e)

            try:
                self.push_price(book['price'])

            except Exception as e:
                print(e)


            time.sleep(2)
            self.save()
            time.sleep(4)
            self.product_list_screen()
            time.sleep(4)
            self.new_product()
            time.sleep(4)


# going to build an interface for testing individual functions

class Interface:
    def __init__(self):
        self.menu_options = '1. iterate all books\n2. iterate by id\n3. individual function \'push img 2\'\nx. Initialise driver'
        self.running = True
        self.all_books = all_books

    def driver_init(self):
        print('initiliasing driver')
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver_2 = webdriver.Chrome('./chromedriver')
        self.driver.get(url)

    def individual_book(self):
        pusher = Pusher(all_books)
        id = input('enter id: ')
        book = pusher.dict[id]

        print(f'id is: {id}')

        pusher.push_title(book['title'])

        pusher.push_description(book['description'])

        pusher.push_imgs(book['img_links'])

        pusher.push_price(book['price'])

        time.sleep(2)
        pusher.save()
        time.sleep(4)
        pusher.product_list_screen()
        time.sleep(4)
        pusher.new_product()
        time.sleep(4)

    def main_loop(self):
        while self.running:
            errors = []
            traces = []
            print(self.menu_options)
            option = input(': ')

            if option == '1':
                try:
                    pusher = Pusher(all_books)
                    pusher.main()
                except Exception as e:
                    print('failed, skipping book & logging error')
                    trace = traceback.format_exc()
                    error = e
                    print(f'\n{trace}\n')
                    print(f'\n{error}\n')
                    traces.append(trace)
                    errors.append(errors)

            if option == '2':
                try:
                    self.individual_book()
                except Exception as e:
                    print(f'\n{traceback.format_exc()}\n')
                    print()
                    print('failed lol')
                    print(str(e))
                    print('')

            if option == '3':
                pusher.push_imgs_2()

            if option == 'x':
                self.driver_init()

            print(errors)
            print(traces)



# class instantiation
read_json = read_json.Json_reader(json_path)
read_json.extract_json()
all_books = read_json.book_dict
interface = Interface()

# img url error = '172091401580'
# unknown error = '182618007165'


interface.main_loop()

# Scrap code

# email_box = self.driver.find_element(By.ID, email_locator)
# email_box.send_keys(email)
# time.sleep(3)
# self.enter(email_box)
# # time.sleep(6)
# password_box = self.driver.find_element(By.ID, pass_locator)
# password = input('enter password\n: ')
# password_box.send_keys(password)
# # time.sleep(6)
