from django.shortcuts import render
from .models import Vacancy


def home_view(requests):  # функция для отображения вакансий
    qs = Vacancy.objects.all()
    context = {
        'object_list': qs
    }
    return render(requests, 'home.html', context)
