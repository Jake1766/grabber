from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
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
failed_books = []


# pause timings
sleep_a = 2
sleep_b = 0.5

# driver = webdriver.Chrome('./chromedriver')
# driver_2 = webdriver.Chrome('./chromedriver')

# errors
# 174686231699 - url f?
# 175624811345 - img fail


class Pusher:
    def __init__(self, dict):
        self.running = True
        self.driver = interface.driver
        self.driver_2 = interface.driver_2
        self.dict = dict
        self.id = ''

    # utility

    def skip_and_log(self):
        print('skipping & logging...')
        print(f'\nbook logged: {self.id}\n')
        file = open('failed_books.txt', 'w')
        failed_books.append(self.id)
        file.write(str(failed_books))
        print('\nrefreshing page...\n')

        try:
            alert = Alert(self.driver)
            alert.accept()
        except:
            print('alert dismiss failed, no alert?')



    def enter(self, element):
        print('pressing enter...\n')
        element.send_keys(Keys.ENTER)

    def push_title(self, title):
        # catch random alert boxes
        tries = 0
        outcome = False
        try:
            alert = self.driver.switch_to.alert
            time.sleep(sleep_b)
            alert.accept()
        except:
            print('\nNo alert box! :)))\n')


        tries = 0
        while tries < 5:
            try:
                print(f'pushing title:\n{title}\n')
                element = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/input')
                element.send_keys(title)
                time.sleep(sleep_a)
                outcome = True
                tries = 5

            except Exception as e:
                time.sleep(5)
                print(e)
                tries += 1

        if outcome == False:
            return outcome
        else:
            return True

    def push_description(self, desc_url):
        tries = 0
        outcome = False
        while tries < 5:
            try:
                print(f'íd test:{self.id}')
                print(f'pushing description from {desc_url}\n')
                self.driver_2.get(desc_url)
                desc_html = self.driver_2.find_element(By.TAG_NAME, 'table')
                desc_html = desc_html.get_attribute('innerHTML')

                # need to press button to write html
                html_button = self.driver.find_element(By.CSS_SELECTOR, "button.edsvs.mQNNA.B1Gi5")
                html_button.click()
                time.sleep(sleep_b)

                # should be able to input raw html now

                desc_box = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/div")
                desc_box.click()
                print('clicked description box...\n')
                pyperclip.copy(desc_html)
                desc_box.send_keys(Keys.CONTROL, 'v')
                print('description added.\n')
                outcome = True
                tries = 5

            except:
                print(f'failed to push description x{tries}')
                tries += 1

        if outcome == False:
            return outcome
        else:
            return True

    #redundant
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
                    outcome = True
                    tries = 5

                except:
                    print(f'failed to click \'add from url\' button x{tries}')
                    outcome = False
                    tries += 1

            if outcome == False:
                return outcome


            tries = 0
            while tries < 5:
                try:
                    entry_field = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[2]/div/section/div/div/div/div[2]/div/div/input')
                    entry_field.click()
                    print('\nentry field select success!\n')
                    outcome = True
                    tries += 5

                except Exception as e:
                    print(f'failed to select entry field x{tries}')
                    print(f'\n{e}\n')
                    print(f'{traceback.format_exc()}\n')
                    outcome = False
                    tries += 1

            if outcome == False:
                return outcome

            tries = 0
            while tries < 5:
                try:
                    entry_field.send_keys(url)
                    print('\nkey send success!\n')
                    outcome = True
                    tries = 5
                except:
                    print(f'failed to enter url x{tries}\n')
                    tries += 1
                    outcome = False

            if outcome == False:
                return outcome

            tries = 0
            while tries < 5:
                try:
                    print('clicking url add button...')
                    submit_url = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[3]/div/div/div[2]/button[2]')
                    submit_url.click()
                    outcome = True
                    tries = 5
                except Exception as e:
                    tries += 1
                    print(f'\nadd url button click attempt x{tries}\n')
                    print(f'{traceback.format_exc}')
                    print(f'\n{e}\n')
                    outcome = False

            if outcome == False:
                return outcome


    def push_imgs_2(self, urls):
        count = 0
        for link in urls:
            print(f'\nimage: {link}\n')

            # check images are present
            if link == 'f':
                print('images failed')
                outcome = False
                return outcome
            # second image check
            if len(link) != 1:
                img_data = requests.get(link).content
                file_path = fr'C:\Users\jaker\Desktop\Migration\temp_images\temp_image_{urls.index(link)}.jpg'
                with open(file_path, 'wb') as handler:
                    handler.write(img_data)
            else:
                return False

        for filename in os.listdir('temp_images'):
            file_path = fr'C:\Users\jaker\Desktop\Migration\temp_images/{filename}'
            print(f'\nfilepath is: {file_path}\n')
            print(f'filename is: {filename}\n')

            tries = 0
            while tries < 5:
                try:
                    print('attempting to click \'add img\' button...')

                    self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[2]/div/div/div[3]/div/div/div[2]/span/input').send_keys(file_path)
                    print('\nsuccess??\n')
                    outcome = True
                    tries = 5

                except Exception as e:
                    print(f'failed to add image x{tries} filepath: {file_path}')
                    print(f'\n{e}\n')
                    print(f'{traceback.format_exc}\n')
                    tries += 1
                    outcome = False
                    if outcome == False:
                        return outcome
            # pause to allow images to upload before deleting
        time.sleep(8)

        for filename in os.listdir('temp_images'):
            file_path = fr'C:\Users\jaker\Desktop\Migration\temp_images/{filename}'
            delete_tries = 0
            while delete_tries < 5:
                try:
                    os.remove(file_path)
                    outcome = True
                    delete_tries = 5


                except Exception as e:
                    delete_tries += 1
                    print(f'failed to delete image at {file_path} x{delete_tries}')
                    print(e)
        if outcome == False:
            return False








        return True

    def push_price(self, price):
        print('pushing price...\n')
        tries = 0
        while tries < 5:
            try:
                price_box = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div')
                price_box.click()
                print('\nsuccess! clicked price box...')
                outcome = True
                tries = 5

            except:
                print('failed to click price box')
                tries += 1
                outcome = False

        if outcome == False:
            return outcome

        tries = 0
        while tries < 5:
            try:
                price_box = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[3]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div/input')
                price_box.send_keys(price)
                print('\nsuccess! sent price...\n')
                outcome = True
                tries = 5

            except:
                print('failed to push price')
                tries += 1
                outcome = False

        if outcome == False:
            return outcome
        else:
            return True

    def save(self):
        print('saving product...')
        tries = 0
        while tries < 5:
            try:
                save_button = self.driver.find_element(By.CSS_SELECTOR, 'button.Polaris-Button_r99lw.Polaris-Button--primary_7k9zs')
                save_button.click()
                print('\nsuccess! product saved...\n')
                outcome = True
                tries = 5
                return outcome

            except:
                tries += 1
                print(f'attempted to save x{tries}')
                outcome = False

        if outcome == False:
            return outcome

    def product_list_screen(self):
        tries = 0
        outcome = False
        while tries < 5:
            try:
                print('navigating to product list screen\n')
                self.driver.get(url)
                # nav_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[1]/div/div/div[1]/div/nav/a')
                # nav_button.click()
                print('\nsuccess!\n')
                tries = 5
                outcome = True
            except:
                print(f'failed to navigate to product screen x{tries}')
                tries += 1

        return outcome





    def new_product(self):
        print('adding new product...\n')
        tries = 0
        while tries < 5:
            try:
                new_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/main/div/div/div[1]/div/div/div[2]/div[2]/div/a')
                new_button.click()
                print('\nsuccess!\n')
                outcome = True
                tries = 5

            except:
                print(f'attempted to navigate to new product... x{tries}')
                tries += 1
                outcome = False

        if outcome == False:
            return outcome


    def main(self):

        input('press enter to start')

        dict = self.dict
        count = 1
        for item in dict:
            outcome = True
            time.sleep(sleep_a)
            print(f'\ntitle {count}\n')

            book = dict[item]
            count += 1

            self.id = item

            print(f'id is: {item}')

            if outcome:
                outcome = self.push_title(book['title'])
            if outcome:
                outcome = self.push_description(book['description'])
            if outcome:
                outcome = self.push_imgs_2(book['img_links'])
            if outcome:
                outcome = self.push_price(book['price'])

            time.sleep(sleep_b)
            if outcome:
                outcome = self.save()

            time.sleep(sleep_a)
            if outcome:
                outcome = self.product_list_screen()
            print(f'failed books:\n{failed_books}')
            if outcome == False:
                status = self.skip_and_log()
                self.driver.refresh()
                time.sleep(5)
                continue


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

        skip_status = pusher.push_imgs_2(book['img_links'])
        if skip_status == 'skip':
            pusher.skip_and_log()
        pusher.push_price(book['price'])

        time.sleep(sleep_b)
        pusher.save()
        time.sleep(sleep_a)
        pusher.product_list_screen()
        time.sleep(sleep_a)
        pusher.new_product()
        time.sleep(sleep_a)

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
# unknown error = '182565881464'
# failed to navigate from: '172666105622'
# failed to navigfate 183113770244


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
