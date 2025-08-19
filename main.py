from scrapper_functions import *


if __name__=='__main__':
    avito_vacancies = scrape_site_for_links("https://career.avito.com/vacancies/data-science/", "div.vacancies-section__item")
    sber_vacancies = scrape_site_for_links_emulate_clicks(
        url="https://rabota.sber.ru/search/",
        target_vac="IT: Data Science и Data Engineering",
        menu_selector='[data-testid="profarea-filter-header"]',
        item_selector='div[class*="styled__Card"]'  # ловим по маске имени класса
    )
    print(avito_vacancies)
    print(sber_vacancies)