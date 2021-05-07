import asyncio
import codecs
import os
import sys
import time
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))  # устанавливаем где директория находится(абсолютный путь)
sys.path.append(proj)  # путь к директории. Добавляем в системные переменные путей.
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"  # устанавливаем в переменные окружения

import django

django.setup()  # можем работать с тем функционалом, который есть в django

from scraping.parsers import *
from scraping.models import City, Language, Vacancy, Error, Url

User = get_user_model()  # функция вернет того пользователя, который определен в настройках Django проекта(
# пользователь по умолчанию  auth_user_model))

# cоздали пару. функция - url
parsers = (
    (head_hunter, 'head_hunter'),
)

# москва# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Python+junior
# спб# https://spb.hh.ru/search/vacancy?clusters=true&area=2&enable_snippets=true&salary=&st'
#                   '=searchVacancy&text=Python+junior+

jobs, errors = [], []


def get_settings():  # получаем данные из user`a
    # функция для набора ключей город-язык программирования. Возврашаем уникальные пары город-язык,
    # по тем пользователям, которые у нас есть в системе
    qs = User.objects.filter(send_email=True).values()  # values позволяет получить список словарей (без instance,
    # без queryset). Получем city_id, language_id
    settings_list = set((q['city_id'], q['language_id']) for q in qs)  # for uniques parameters
    return settings_list  # получаем пару: город-язык {(3, 1), (2, 1)}


def get_urls(settings):  # список с набором url, для передачи в функцию scraping
    qs = Url.objects.all().values()  # запрос к БД. => values превращает данные в id
    url_dict = {
        (q['city_id'], q['language_id']): q['url_data'] for q in qs  # ключ(cоставной) - tuple
        # по составному ключу, из полученных settings составим набор url для функции
    }
    urls = []
    for pair in settings:  # {(3,1), (2,1)}
        if pair in url_dict:  # проверка на существование ключа
            tmp = {
                'city': pair[0],
                'language': pair[1],
                'url_data': url_dict[pair]
            }

        urls.append(tmp)  # получим значения, которые необходимы
    return urls


async def main(value):
    func, url, language, city = value  # получим значения
    job, err = await loop.run_in_executor(None, func, url, language, city)  # запускаем на выполнение
    errors.extend(err)
    jobs.extend(job)

setting = get_settings()
url_list = get_urls(setting)

# city = City.objects.filter(slug='moskva').first()  # first() => перевели из QuerySet`a в Instanse
# language = Language.objects.filter(slug='python').first()


start = time.time()
loop = asyncio.get_event_loop()  # запуск задач
tmp_tasks = [  # cоздали список с полным набором всех необходимых выполнений функций
    (func, data['url_data'][key], data['language'], data['city'])
    for data in url_list
    for func, key in parsers
]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])  # запуск на выполнение. Создаем task на запуск

# for data in url_list: # теперь логика в async
#     for func, key in parsers:
#         url = data['url_data'][key]  # получаем url из модели Url
#         j, e = func(url, language=data['language'],
#                     city=data['city'])  # раскладываем в разные переменные для последующего добавления в списки
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

print(time.time() - start)
for job in jobs:
    v = Vacancy(**job, )
    try:
        v.save()
    except DatabaseError:  # url должен быть уникальным. Используем try, except
        pass
if errors:  # если ошибки существуют
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors: {errors}').save()  # в модель добавляем значение поля data

h = codecs.open('work_parser1.txt', 'w', 'utf-8')
h.write(str(jobs))  # получаем контент от сервера. Преобразуя байты в строки
h.close()

