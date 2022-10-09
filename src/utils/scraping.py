from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


from itertools import islice
from fake_useragent import UserAgent
from joblib import Parallel, delayed

import time
import pandas as pd
import numpy as np
import re
import json
import warnings
import json
import random
import string
import unidecode

warnings.filterwarnings('ignore')

PATH_CHROME = '/home/gary/Apps/chromedriver'
PATH_INTERMEDIATE = '../../data/intermediate/'

# ----------------------------------------------------------------------
# fields x districts approach

def get_fields_districts_dicts():
    driver = webdriver.Chrome(PATH_CHROME)
    driver.get('https://www.lkcr.cz/seznam-lekaru-426.html#seznam')

    ## dict of fields - name:value
    d_fields = dict()

    filterObor = driver.find_element_by_name('filterObor')
    options = [x for x in filterObor.find_elements_by_tag_name("option")]

    for element in options:
        if element.text:
            d_fields[element.text] = element.get_attribute("value")

    ## dict of districts - name:value
    d_districts = dict()

    filterOkresId = driver.find_elements_by_name('filterOkresId')[-1]

    options = [x for x in filterOkresId.find_elements_by_tag_name("option")]

    for element in options:
        if element.text:
            d_districts[element.text] = element.get_attribute("value")

    driver.close()
    
    np.save(PATH_DATA+'dict_districts.npy', d_districts) 
    np.save(PATH_DATA+'dict_fields.npy', d_fields) 
    return d_fields, d_districts


def set_viewport_size(driver, width, height):
    '''
        Sets width and height of the webpage. It can help to bypass CAPTCHA
    '''
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

    

def chunks(d, SIZE=10):
    '''
     Split dictionary into chunks of SIZE
    '''
    it = iter(data)
    for i in range(0, len(d), SIZE):
        yield {k:d[k] for k in islice(it, SIZE)}
            

def save_progress(processed_letters, finished_letters):
    with open(PATH_INTERMEDIATE+'finished_letters.txt','w') as f:
        f.write(str(finished_letters))

    np.save(PATH_INTERMEDIATE+'processed_letters.npy', processed_letters) 

def load_progress():
    '''
     Load info about already processed substrings in CLK search.
     Returns:
         processed_letters: already processed substrings
         finished_letters: completely processed first letters from the alphabet
    '''
    import ast
    with open(PATH_INTERMEDIATE+'finished_letters.txt','r') as f:
        finished_letters = ast.literal_eval(f.read())

    processed_letters = np.load(PATH_INTERMEDIATE+'processed_letters.npy',allow_pickle='TRUE').item()
    return processed_letters, finished_letters

    
def get_surname(full_name):
    names = full_name.split()
    if ',' in names[-2]:
        return names[-2][:-1]
    else:
        return names[-1]   
    
## ------------------------------------------------------           
def obtain_links(d_districts, d_fields):
    l_info = [] # general info about doctors
    processed_options = []

    try:
        # iterate over districts
        for district_name, district_id in d_districts.items():

            # iterate over fields
            for field_name, field_id in d_fields.items():

                # https://stackoverflow.com/questions/58872451/how-can-i-bypass-the-google-captcha-with-selenium-and-python
                # set fake agent
                options = Options()
                user_agent = UserAgent().random
                options.add_argument(f'user-agent={user_agent}')
                # TODO check user_agent's validity 
                driver = webdriver.Chrome(executable_path=PATH_CHROME, chrome_options=options)

                # mouseover actions
                action_chains = ActionChains(driver)

                # randomly change size of the webpage
                set_viewport_size(driver, random.randrange(950, 1300), random.randrange(600, 800))

                driver.get('https://www.lkcr.cz/seznam-lekaru-426.html#seznam')

                time.sleep(1)

                # mouseover to reject cookies
                reject = driver.find_element(By.CLASS_NAME, 'cc-nb-reject') #.click()
                ActionChains(driver).move_to_element(reject).click().perform()


                # select district
                wait = WebDriverWait(driver, 2)
                select = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='filterOkresId']")))
                action_chains.move_to_element(select).click().perform()
                time.sleep(1)

                select_d = Select(select)
                select_d.select_by_value(district_id)

                # select field of medicine
                select = wait.until(EC.element_to_be_clickable((By.NAME, "filterObor")))
                action_chains.move_to_element(select).click().perform()
                time.sleep(1)

                select_f = Select(select)
                select_f.select_by_value(field_id)

                # Confirm chosen options and search
                wait.until(EC.element_to_be_clickable((By.NAME, "do[findLekar]=1")))
                time.sleep(.5)
    #             action_chains.move_to_element(search).click().perform()
                search = driver.find_element_by_name('do[findLekar]=1')
                search.send_keys(Keys.RETURN)
    #             search.click()

                time.sleep(4)

                # Page counter
                counter = 0
                while True: 
                    # Stopping criteria
                    next_page_text = f'{counter*20+1}-{counter*20+20}'
                    if not next_page_text in driver.page_source and not 'Další >>' in driver.page_source:
                        break

                    driver.get(f'https://www.lkcr.cz/seznam-lekaru-426.html?paging.pageNo={counter}')
                    main = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "form-clk"))
                    )
                    doc_list = main.find_element(by=By.CLASS_NAME, value='seznam-lekaru.item-list')

                    for i in doc_list.find_elements(by=By.CLASS_NAME, value='item')[1:]:
                        info = i.text.split('\n')[:-1]
                        link = i.find_element_by_css_selector('a').get_attribute('href')
                        info = [link, district_name, field_name] + info 
                        l_info.append(info)

                    # next page
                    counter += 1

                driver.close()

    finally:
        return l_info









# ----------------------------------------------------------------------
# names approach

