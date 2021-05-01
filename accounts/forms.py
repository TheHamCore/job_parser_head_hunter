from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()  # функция вернет того пользователя, который определен в настройках Django проекта(


# пользователь по умолчанию  auth_user_model))

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form_control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_control'}))

    def clean(self, *args, **kwargs):  # данный метод есть по умолчанию в каждой форме. Для ПРОВЕРКИ данных в форме. Cрабатывает сразу же при отправке формы
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)  # проверяем, есть ли у нас такой пользователь
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя не существует')
            if not check_password(password, qs[0].password):  # функция преобразовывает пароль, к зашифрованному состоянию и проверяет равен ли он паролю, полученному в фильтре
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(email=email, password=password)  # аутентифицируем
            if not user:  # если отключили аккаунт(неактивный пользователь)
                raise forms.ValidationError('Данный аккаунт отключен')

        return super(UserLoginForm, self).clean(*args, **kwargs)
