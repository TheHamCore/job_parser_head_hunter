from django.db import models

from scraping.utils import from_cyrillic_to_eng


class City(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название населенного пункта',
                            unique=True)
    slug = models.CharField(max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # если slug не заполнен
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)  # если slug


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    timestamp = models.DateField(auto_now_add=True)  # день, когда внесена вакансия
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')  # много вакансий к 1 городу
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')  # много вакансий к 1 ЯП

    class Meta:
        verbose_name = 'Вакансию'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title
