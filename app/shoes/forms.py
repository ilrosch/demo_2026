from django import forms
from django.contrib.auth.models import User
from shoes.models import Products


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


class ProductForm(forms.ModelForm):
    """Форма добавление/редактирования товара"""

    class Meta:
        model = Products
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)