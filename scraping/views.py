from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):  # функция для отображения вакансий
    # print(requests.GET)
    # print(requests.POST)
    form = FindForm()  # подгрузили форму

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):  # функция для отображения вакансий
    # print(requests.GET)
    # print(requests.POST)
    form = FindForm()  # подгрузили форму

    city = request.GET.get('city')
    language = request.GET.get('language')
    # qs = []

    if city or language:
        _filter = {}  # словарь, который передаем в фильтр
        if city:
            _filter['city__slug'] = city  # Поиск, который использует отношения(документация)
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)  # раскрываем словарь с параметрами

        paginator = Paginator(qs, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'object_list': page_obj,
        'city': city,
        'language': language,
        'form': form,
    }
    return render(request, 'scraping/list.html', context)