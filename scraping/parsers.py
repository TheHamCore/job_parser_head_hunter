import requests
import codecs
from bs4 import BeautifulSoup
from random import randint

__all__ = ('head_hunter',)  # для ипорта всех последующий функций.



headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def head_hunter(url, language=None, city=None):
    jobs = []
    errors = []
    if url:  # если url есть в списке.
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')

            main_div = soup.find('div', attrs={'class':'vacancy-serp'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class':'vacancy-serp-item'})

                for div in div_list:
                    title = div.find('span', attrs={'class':'g-user-content'})
                    href = title.a['href']  # используем точечную нотацию
                    description = div.find('div', attrs={'class': 'g-user-content'})
                    description1 = description.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
                    description2 = description1.text
                    company = div.find('a', attrs={'class': 'bloko-link bloko-link_secondary'})
                    # subway = div.find('span', attrs={'class':'metro-point'})
                    jobs.append({
                        'title': title.text,
                        'url': href,
                        'description': description2,
                        # 'description_responsibility': description_responsibility,
                        # 'description_requirement': description_requirement.text,
                        'company': company.text,
                        # 'subway': subway,
                        'city_id': city,
                        'language_id': language
                    })
            else:
                errors.append({
                    'url': url,
                    'title': 'Страница не отвечает. Не найден главный блок(div)'
                })
        else:
            errors.append({
                'url': url,
                'title': 'Страница не отвечает'
            })

    return jobs, errors


# h = codecs.open('work.html', 'w', 'utf-8')  # сервер присылает ответ
# h.write(str(resp.text))  # записываем байты в строки
# h.close()

if __name__ == '__main__':
    url = 'https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text=python'
    jobs, errors = head_hunter(url)
    h = codecs.open(u''+'../work_parser1.txt', 'w', encoding="utf-8")  # сервер присылает ответ
    h.write(str(jobs))  # записываем байты в строки
    h.close()
