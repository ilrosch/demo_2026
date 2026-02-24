import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from shoes.forms import LoginForm, ProductForm
from shoes.models import Products, Providers, Users


def login_page(req):
    """Авторизация в системе"""

    if req.method == 'POST':
        form = LoginForm(req.POST)

        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, f'Добро пожаловать, {user.get_full_name() or user.username}!')
            return redirect('main:products')
        else:
            messages.error(req, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(
        request=req,
        template_name='login.html',
        context={
            'title': 'Авторизация',
            'form': form,
        }
    )


def logout_page(req):
    """Выход из системы"""

    logout(req)
    messages.success(req, 'Вы успешно вышли из системы.')
    return redirect('main:login')


def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    return 'user'


def products_page(req):
    """Каталог товаров"""

    user_role = get_user_role(req.user)
    providers = Providers.objects.all()

    products = Products.objects.select_related('category', 'provider', 'producer', 'unit')

    if user_role in ['manager', 'admin']:
        search_value = req.GET.get('search', '')
        if search_value:
            products = products.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(provider__name__icontains=search_value) |
                Q(producer__name__icontains=search_value)
            )

        provider_filter = req.GET.get('provider', '') 
        if provider_filter:
            products = products.filter(provider__name=provider_filter)

        sort_by = req.GET.get('sort', 'name-asc')
        match sort_by:
            case 'name-asc':
                products = products.order_by('name')
            case 'name-desc':
                products = products.order_by('-name')
            case 'price-asc':
                products = products.order_by('price')
            case 'price-desc':
                products = products.order_by('-price')
            case 'amount-asc':
                products = products.order_by('amount')
            case 'amount-desc':
                products = products.order_by('-amount')
            case _:
                products = products.order_by('name')
        
    else:
        search_value = ''
        provider_filter = ''
        sort_by = ''

    paginator = Paginator(products, 10)
    page_num = req.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(
        request=req,
        template_name='products.html',
        context={
            'title': 'Каталог товаров',
            'user': req.user,
            'user_role': user_role,
            'page_obj': page_obj,
            'providers': providers,
            'sort_by': sort_by,
            'search_value': search_value,
            'provider_filter': provider_filter,
        }
    )


@login_required
def product_create_page(req):
    """Добавление товара (только для администратора)"""

    user_role = get_user_role(req.user)
    if user_role not in 'admin':
        messages.info(req, 'Действие только для администратора!')
        return redirect('main:products')

    if req.method == 'POST':
        form = ProductForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            messages.success(req, 'Товар добавлен успешно!')
            return redirect('main:products')
    else:
        form = ProductForm()

    return render(
        request=req,
        template_name='product.html',
        context={
            'title': 'Добавление товара',
            'form': form,
        }
    )


@login_required
def product_update_page(req, pk):
    """Редактирование товара (только для администратора)"""

    user_role = get_user_role(req.user)
    if user_role not in 'admin':
        messages.info(req, 'Действие только для администратора!')
        return redirect('main:products')

    product = get_object_or_404(Products, pk=pk)
    old_product = copy.deepcopy(product)

    if req.method == 'POST':
        form = ProductForm(req.POST, req.FILES, instance=product)
        if form.is_valid():
            # Удаление фото при добавление новой или очистке старой
            if ('image' in req.FILES and old_product.image) or req.POST.get('image-clear') == 'on':
                old_product.image.delete()
            form.save()
            messages.success(req, 'Товар обновлен успешно!')
            return redirect('main:products')
    else:
        form = ProductForm(instance=product)

    return render(
        request=req,
        template_name='product.html',
        context={
            'title': 'Редактирование товара',
            'form': form,
        }
    )


@login_required
def product_delete(req, pk):
    """Удаление товара (только для администратора)"""

    user_role = get_user_role(req.user)
    if user_role not in 'admin':
        messages.info(req, 'Действие только для администратора!')
        return redirect('main:products')

    product = get_object_or_404(Products, pk=pk)
    product.delete()
    messages.success(req, 'Товар успешно удален!')
    return redirect('main:products')