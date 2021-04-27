import os
import sys
from django.db import DatabaseError
proj = os.path.dirname(os.path.abspath('manage.py'))  # устанавливаем где директория находится(абсолютный путь)
sys.path.append(proj)  # путь к директории. Добавляем в системные переменные путей.
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"  # устанавливаем в переменные окружения

import django
django.setup()  # можем работать с тем функционалом, который есть в django


from scraping.parsers import *
from scraping.models import City, Language, Vacancy

# cоздали пару. функция - url
parsers = (
    (head_hunter, 'https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text=python'),
)

city = City.objects.filter(slug='sankt-peterburg').first()  # first() => перевели из QuerySet`a в Instanse
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)  # раскладываем в разные переменные для последующего добавления в списки
    jobs += j
    errors += e

print(jobs)
for job in jobs:
    v = Vacancy(**job, language=language, city=city, )
    try:
        v.save()
    except DatabaseError:  # url должен быть уникальным. Используем try, except
        pass

h = open('work.txt', 'w', encoding='utf-8')
h.write(str(jobs))  # получаем контент от сервера. Преобразуя байты в строки
h.close()