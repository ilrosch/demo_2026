from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    """Форма авторизации"""

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

