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
        time.sleep(4)
        desc_box.send_keys(desc_html)
        input('enter any key to exit\n: ')

    def push_imgs(self):
        pass

    def push_price(self):
        pass


    def main(self):
        self.driver.get(url)
        input('press enter to start')

        dict = self.dict
        for item in dict:

            book = dict[item]

            self.push_title(book['title'])

            self.push_description(book['description'])

            time.sleep(60)






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
