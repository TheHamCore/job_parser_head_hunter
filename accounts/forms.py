from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()  # функция вернет того пользователя, который определен в настройках Django проекта(


# пользователь по умолчанию  auth_user_model))

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form_control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_control'}))

    def clean(self, *args,
              **kwargs):  # данный метод есть по умолчанию в каждой форме. Для ПРОВЕРКИ данных в форме. Cрабатывает сразу же при отправке формы
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)  # проверяем, есть ли у нас такой пользователь
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя не существует')
            if not check_password(password, qs[
                0].password):  # функция преобразовывает пароль, к зашифрованному состоянию и проверяет равен ли он паролю, полученному в фильтре
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(email=email, password=password)  # аутентифицируем
            if not user:  # если отключили аккаунт(неактивный пользователь)
                raise forms.ValidationError('Данный аккаунт отключен')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Введите email', widget=forms.EmailInput(attrs={'class': 'form_control'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form_control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form_control'}))

    class Meta:
        model = User  # cоздали форму на основе модели user => она подтягивает данные для проверки, которые указаны в
        # этой форме (email дб уникальным)
        fields = ('email',)

    def clean_password2(self):  # данный метод будет вызван в любом случае(проверка на совпадение 2 паролей)
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадает')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Город"
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Язык программирования"
    )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Получать рассылку?')

    class Meta:
        model = User  # cоздали форму на основе модели user => она подтягивает данные для проверки, которые указаны в
        # этой форме (email дб уникальным)
        fields = ('city', 'language', 'send_email')


class ContactForm(forms.Form):
    city = forms.CharField(
        required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.CharField(
        required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    email = forms.EmailField(
        label='Введите email адрес', required=True, widget=forms.EmailInput(
                                 attrs={'class': 'form-control'})
    )