from django.urls import path, include
from shoes import views


app_name = 'main'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('products/', views.products_page, name='products'),
    path('product/', include([
        path('create/', views.product_create_page, name='product_create'),
        path('update/<int:pk>/', views.product_update_page, name='product_update'),
        path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    ]))
]