from scrapper_functions import *
import importlib
import db
importlib.reload(db)
from db import *

if __name__=='__main__':
    avito_vacancies = scrape_site_for_links("https://career.avito.com/vacancies/data-science/", "div.vacancies-section__item")
    sber_vacancies = scrape_site_for_links_emulate_clicks(
        url="https://rabota.sber.ru/search/",
        target_vac="IT: Data Science и Data Engineering",
        menu_selector='[data-testid="profarea-filter-header"]',
        item_selector='div[class*="styled__Card"]'  # ловим по маске имени класса
    )

    db_init()

    print(avito_vacancies)
    print(sber_vacancies)

    for item in avito_vacancies:
        add_to_db(url=item['url'], title=item['title'], company='Avito')
    for item in sber_vacancies:
        add_to_db(utl=item['url'], title=item['title'], company='Sber')