from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import read_json

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


class Pusher:
    def __init__(self, dict):
        self.running = True
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver_2 = webdriver.Chrome('./chromedriver')
        self.dict = dict

    # utility

    def enter(self, element):
        print('pressing enter...\n')
        element.send_keys(Keys.ENTER)

    def push_title(self, title):
        print(f'pushing title:\n{title}\n')
        element = self.driver.find_element(By.ID, title_locator)
        element.send_keys(title)
        time.sleep(3)

    def push_description(self, desc_url):
        print(f'pushing description from {desc_url}\n')
        self.driver_2.get(desc_url)
        desc_html = self.driver_2.find_element(By.TAG_NAME, 'table')
        desc_html = desc_html.get_attribute('innerHTML')
        print(type(desc_html))
        print(f'html is:\n{desc_html}\n')

        # need to press button to write html
        html_button = self.driver.find_element(By.CSS_SELECTOR, "button.OIVe2.ISVaC.j3vXR")
        html_button.click()
        time.sleep(2)

        # should be able to input raw html now

        desc_box = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/main/div/div/div[2]/form/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/div")
        # self.driver.execute_script(f"document.getElementById('product-description').innerHTML={desc_html};")
        desc_box.click()
        print('clicked description box...\n')
        desc_box.send_keys(desc_html)
        print('description added.\n')


    def push_imgs(self, array):
        print(f'urls:\n{array}')
        for url in array:
            # need to press button to open entry field for url
            print(f'adding url: {url}\n')
            tries = 0
            while tries < 5:
                try:
                    url_add_button = self.driver.find_element(By.CLASS_NAME, 'Polaris-Link_yj5sy')
                    url_add_button.click()
                    tries += 5

                except:
                    print(f'failed to click \'add from url\' button x{tries}')
                    tries += 1

            tries = 0
            while tries < 5:
                try:
                    entry_field = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[2]/div/section/div/div/div/div[2]/div/div/input')
                    entry_field.click()
                    tries += 5

                except:
                    print(f'failed to select entry field x{tries}')
                    tries += 1

            entry_field.send_keys(url)


            submit_url = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[14]/div[1]/div/div/div/div/div[3]/div/div/div[2]/button[2]/span/span')
            submit_url.click()

    def push_price(self, price):
        price_box = self.driver.find_element(By.ID, 'PolarisTextField40')
        price_box.send_keys(price)

    def save(self):
        print('saving product...')
        save_button = self.driver.find_element(By.CSS_SELECTOR, 'button.Polaris-Button_r99lw.Polaris-Button--primary_7k9zs')
        save_button.click()

    def product_list_screen(self):
        print('navigating to product list screen\n')
        nav_button = self.driver.find_element(By.CLASS_NAME, 'Polaris-Breadcrumbs__Breadcrumb_llsun')
        nav_button.click()

    def new_product(self):
        print('adding new product...\n')
        save_button = self.driver.find_element(By.CSS_SELECTOR, 'button.Polaris-Button_r99lw.Polaris-Button--primary_7k9zs')
        save_button.click()

    def main(self):
        self.driver.get(url)
        input('press enter to start')

        dict = self.dict

        for item in dict:

            book = dict[item]

            self.push_title(book['title'])

            self.push_description(book['description'])

            self.push_imgs(book['img_links'])

            self.push_price(book['price'])

            self.product_list_screen()

            self.new_product()

            self.save()







read_json = read_json.Json_reader(json_path)
read_json.extract_json()
pusher = Pusher(read_json.book_dict)
pusher.main()



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
