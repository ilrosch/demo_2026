from django.urls import path
from shoes import views


app_name = 'main'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('products/', views.products_page, name='products'),

]
