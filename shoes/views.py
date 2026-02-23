from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from shoes.forms import LoginForm
from shoes.models import Products


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
    messages.info(req, 'Вы успешно вышли из системы.')
    return redirect('main:login')


def get_user_role(user):
    if not user.is_authenticated:
        return 'gust'
    if user.is_superuser:
        return 'admin'
    return 'user'


def products_page(req):
    """Каталог товаров"""

    user_role = get_user_role(req.user)
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
            'products': products,
            'sort_by': sort_by,
            'search_value': search_value,
        }
    )


# def login_view(request):
#     """Представление для входа в систему"""
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f'Добро пожаловать, {user.get_full_name() or user.username}!')
#             return redirect('products:product_list')
#         else:
#             messages.error(request, 'Неверное имя пользователя или пароль.')

#     return render(request, 'accounts/login.html')


# def logout_view(request):
#     """Представление для выхода из системы"""
#     logout(request)
#     messages.info(request, 'Вы успешно вышли из системы.')
#     return redirect('accounts:login')


# @login_required
# def profile_view(request):
#     """Представление профиля пользователя"""
#     return render(request, 'accounts/profile.html')