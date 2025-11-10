from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category
from datetime import datetime, timedelta
from django.utils import timezone

def home(request):
    """Главная страница"""
    # Получаем новинки (товары за последние 7 дней) - только 3 штуки
    new_products = Product.objects.filter(
        is_available=True,
        created_at__gte=timezone.now() - timedelta(days=7)
    )[:4]
    
    # Получаем популярные товары - только 3 штуки
    popular_products = Product.objects.filter(
        is_available=True
    ).order_by('-orders_count')[:4]
    
    context = {
        'new_products': new_products,
        'popular_products': popular_products,
    }
    return render(request, 'shop/home.html', context)

def about(request):
    """Страница О нас"""
    return render(request, 'shop/about.html')

def contacts(request):
    """Страница Контакты"""
    return render(request, 'shop/contacts.html')

def product_list(request):
    # Получаем все товары
    products = Product.objects.filter(is_available=True)
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Фильтрация по диапазону цен
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Фильтрация по дате добавления
    date_filter = request.GET.get('date_filter')
    if date_filter:
        if date_filter == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            products = products.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            products = products.filter(created_at__gte=month_ago)
    
    # Сортировка
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.order_by('-orders_count')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:
        products = products.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(products, 10)  # 10 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'date_filter': date_filter,
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    """Представление для детальной страницы товара"""
    product = get_object_or_404(Product, pk=pk, is_available=True)
    
    # Похожие товары (из той же категории)
    similar_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'shop/product_detail.html', context)

def ajax_product_list(request):
    """AJAX view для обновления списка товаров без перезагрузки страницы"""
    products = Product.objects.filter(is_available=True)
    
    # Применяем те же фильтры, что и в основном view
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    date_filter = request.GET.get('date_filter')
    if date_filter:
        if date_filter == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            products = products.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            products = products.filter(created_at__gte=month_ago)
    
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.order_by('-orders_count')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:
        products = products.order_by('-created_at')
    
    # Пагинация для AJAX
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Подготавливаем данные для JSON
    products_data = []
    for product in page_obj:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'category': product.category.name,
            'image_url': product.image.url if product.image else '',
            'created_at': product.created_at.strftime('%d.%m.%Y'),
            'orders_count': product.orders_count,
            'description': product.description[:100] + '...' if len(product.description) > 100 else product.description,
        })
    
    return JsonResponse({
        'products': products_data,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
    })