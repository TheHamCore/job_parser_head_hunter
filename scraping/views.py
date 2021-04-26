from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):  # функция для отображения вакансий
    # print(requests.GET)
    # print(requests.POST)
    form = FindForm()  # подгрузили форму

    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []

    if city or language:
        _filter = {}  # словарь, который передаем в фильтр
        if city:
            _filter['city__slug'] = city  # Поиск, который использует отношения(документация)
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)  # раскрываем словарь с параметрами
    context = {
        'object_list': qs,
        'city': city,
        'language': language,
        'form': form
    }
    return render(request, 'scraping/home.html', context)
