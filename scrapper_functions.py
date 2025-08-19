import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from exceptions import NoItemsError, AttributeExtractionError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random

SCHEDULE = (1, 2)

with open('json_data\\agents.json', 'r', encoding='utf-8') as file:
    agents = json.load(file)

agents['USER_AGENTS']
user_agent = agents['USER_AGENTS']


def scrape_site_for_links(url, item_selector):
    '''
    Simple scraper that gets a complete URL with the selected interests
    '''
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)

    link_list = []

    try:
        driver.get(url)
        time.sleep(random.uniform(SCHEDULE[0], SCHEDULE[1]))
        items = driver.find_elements(By.CSS_SELECTOR, item_selector)
        if not items:
            raise NoItemsError(f"No items found on {url}")
        
        for element in items:
            a_tag = element.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            title = element.text.strip()
            if href:
                link_list.append({"title": title, "url": href})
            else:
                raise AttributeExtractionError(f"No href in element on {url}")
            
    except Exception as e:
        raise e
    
    finally:
        driver.quit()
        
    return link_list


def read_page_for_content(url, item_selector):
    '''
    
    '''
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)

    text_list = []

    try:
        driver.get(url)
        time.sleep(random.uniform(SCHEDULE[0], SCHEDULE[1]))
        sections = driver.find_elements(By.CSS_SELECTOR, item_selector)

        if not sections:
            raise NoItemsError(f"No sections found on {url}")

        for section in sections:
            # Берём весь текст секции целиком
            section_text = section.text.strip()
            if section_text:
                text_list.append(section_text)

    except Exception as e:
        raise e
    
    finally:
        driver.quit()
        
    return text_list


def scrape_site_for_links_emulate_clicks(url, target_vac, menu_selector, item_selector):
    '''
    url: str - link to the site
    target_vac: str - prof area selection
    menu_selector: str - menu class
    item_selector: str - individual vacancy class
    '''

    options = Options()

    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")

    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    link_list = []

    try:
        driver.get(url)
        time.sleep(2)

        menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, menu_selector)))
        menu.click()
        time.sleep(1)

        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{target_vac}')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", option)
        option.click()
        time.sleep(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(SCHEDULE[0], SCHEDULE[1]))

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        items = driver.find_elements(By.CSS_SELECTOR, item_selector)
        for item in items:
            try:
                a_tag = item.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
                title = item.text.strip()
                if href:
                    link_list.append({"title": title, "url": href})
            except:
                continue

    finally:
        driver.quit()

    return link_list
