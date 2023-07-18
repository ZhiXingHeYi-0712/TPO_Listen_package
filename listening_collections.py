import requests
from bs4 import BeautifulSoup

def extract_TPO_code_and_link_from_tag(tag):
    tpo_title = tag.get('data-title').split(' ')
    link = 'https://toefl.kmf.com' + tag.find('a', class_='listen-exam-link button-style js-listen-link').get('href')

    tpo_code = int(tpo_title[1])
    set_code = int(tpo_title[-1])

    return link, tpo_code, set_code

def getListeningPagesInCollection(index_page):
    content = requests.get(index_page).content
    b = BeautifulSoup(content, features='lxml')

    return [extract_TPO_code_and_link_from_tag(i) for i in b.find_all('div', class_='practice-lists js-practice-lists')]

def getAllListeningPages():
    result = []
    for i in range(1, 12):
        index_page_url = f'https://toefl.kmf.com/listen/ets/order/{i}/0'

        result.extend(getListeningPagesInCollection(index_page_url))

    return result


