# Generated by Django 3.1.7 on 2021-05-08 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='description',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='subway',
        ),
    ]