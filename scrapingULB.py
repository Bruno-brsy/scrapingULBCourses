import requests
import bs4
import re

ALL_COURSES = {} # struc [["cours", [liste de fac (ou cursus?) dans laquel ce trouve le cours]], ["cours", [liste de fac (ou cursus?) dans laquel ce trouve le cours]]]
ALL_CURSUS = []


def request_web_page(webPage: str):
    r = requests.get(webPage)
    if r.status_code != 200:
        exit(-1)
    return bs4.BeautifulSoup(r.content, 'html.parser')


def find_programs_from_page(coursesWebPage: bs4.BeautifulSoup):
    s = coursesWebPage.find_all('div', class_='search-result__informations')
    for i in s:
        for j in i.contents:
            if isinstance(j, bs4.element.Tag):
                for k in list(j.attrs.values()):
                    if re.search('^https://www\.ulb\.be/fr/programme.*$', str(k)):
                        ALL_CURSUS.append(k)


def find_all_programs(page: str):
    lastPage = False
    while not lastPage:
        lastPage = True
        coursesWebPage = request_web_page(page)

        s = coursesWebPage.find_all('div', class_='search-result__pagination')
        for i in range(1, len(s[0].contents), 2):
            if s[0].contents[i].contents[0] == 'Page suivante':
                page = 'https://www.ulb.be' + s[0].contents[i].attrs['href']
                lastPage = False

        find_programs_from_page(coursesWebPage)



find_all_programs('https://www.ulb.be/servlet/search?l=0&beanKey=beanKeyRechercheFormation&&types=formation&s=FACULTE_ASC&limit=10&page=1')

print(ALL_CURSUS, len(ALL_CURSUS))