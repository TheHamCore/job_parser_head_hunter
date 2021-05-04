import os
import sys
import django
from django.contrib.auth import get_user_model
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))  # устанавливаем где директория находится(абсолютный путь)
sys.path.append(proj)  # путь к директории. Добавляем в системные переменные путей.
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"  # устанавливаем в переменные окружения

django.setup()
from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = "Рассылка вакансий за {today}"
text_content = "Рассылка вакансий {today} "
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по вашим предпочтениям данных нет</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
    # cформировали словарь с ключом: id города и языка и значение с набором
    # email`ов для этой пары.

print(users_dict)

if users_dict:
    params = {
        'city_id__in': [],  # находим все значения, которые принадлежат паре
        'language_id__in': []
    }
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])  # получаем значения из БД по всем необходимым городам для рассылки
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'], i['language_id'])].append(i)
    #
    # for keys, emails in users_dict.items():
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:  # формируем html content
    #         html += f'<h5><a href="{ row["url"] }">{ row["title"] }</a></h5>'
    #         html += f'<p>{row["description_requirement"]}</p>'
    #         html += f'<p>{row["company"]}</p><br><hr>'
    #     html = html if html else empty
    #     for email in emails:
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(html, "text/html")
    #         msg.send()

subject = ''
text_content = ''
to = ADMIN_USER  # Отправка письма администратору об ошибках
html = ''

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    # print(error)
    data = error.data.get('errors', [])  # получаем весь набор значений, которые есть в списке
    for i in data:
        html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p><br>'
    subject = f'Ошибки скрапинга {today}'
    text_content = f'Ошибки скрапинга'

    data = error.data.get('user_data', [])  # получаем весь набор значений, которые есть в списке
    if data:
        html += '<hr>'
        html += '<h2>Пожелание пользователей</h2>'
        for i in data:
            html += f'<p>Город: {i["city"]}, ' \
                    f'Cпециальность: {i["language"]},' \
                    f'Email: {i["email"]}</p><br>'
        subject = f'Пожелания пользователей {today}'
        text_content = f'Пожелания пользователей'

qs = Url.objects.all().values('city', 'language')
urls_dict = {(i['city'], i['language']): True for i in qs}  # составим словарь с ключами city, language
urls_errors = ''

for keys in users_dict.keys():  # проверяем совпадают ли ключи в urls и в users
    if keys not in urls_dict:  # если нет, следовательно не хватает url
        if keys[0] and keys[1]:
            urls_errors = f'<p>Для города:{keys[0]} и языка программирования {keys[1]} отсутствуют urls</p><br>'
if urls_errors:
    subject += 'Отсутствующие urls'
    html += urls_errors
if subject:
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
# print(vacancies)
#
# print(params)
#
# print(html)
