from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

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


# class VList(ListView):
#     model = Vacancy  #
#     template_name = 'scraping/list.html'
#     form = FindForm()  # подгрузили форму
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):  # добавления значения в контекст. Настройки для context
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context['language'] = self.request.GET.get('city')  # получаем request через self
#         context['city'] = self.request.GET.get('language')
#         context['form'] = self.form
#
#         return context
#
#     def get_queryset(self):  # переопределяем поведения queryset(filter и тд)
#         city = self.request.GET.get('city')
#         language = self.request.GET.get('language')
#         qs = []
#         if city or language:
#             _filter = {}  # словарь, который передаем в фильтр
#             if city:
#                 _filter['city__slug'] = city  # Поиск, который использует отношения(документация)
#             if language:
#                 _filter['language__slug'] = language
#             qs = Vacancy.objects.filter(**_filter)  # раскрываем словарь с параметрами
#         return qs


# def v_detail(request, pk):
#     # object_v = Vacancy.objects.get(pk=pk)
#     object_v = get_object_or_404(Vacancy, pk=pk)
#     return render(request, 'scraping/detail.html', {'object_v': object_v})


class VDetail(DetailView):
    queryset = Vacancy.objects.all()  # переопределям, на случай использования filter
    template_name = 'scraping/detail.html'  # параметр, который необходимо задать если нужно подключить свой шаблон.
    # (по умолчанию формируется Vacancy_detail)
    context_object_name = 'object_v'  # параметр. По умолчанию => object

    # def get(self, request, *args, **kwargs):  # в случаях переопределения метода get
    #     pass


class VCreate(CreateView):
    model = Vacancy
    fields = '__all__'  # передача набора полей в нашей таблице (Vacansy)
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')