from django.urls import path
from . import views


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('product_list/', views.product_list, name='product_list'),  # Каталог товаров
    path('about/', views.about, name='about'),  # О нас
    path('contacts/', views.contacts, name='contacts'),  # Контакты
    path('ajax-product-list/', views.ajax_product_list, name='ajax_product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]