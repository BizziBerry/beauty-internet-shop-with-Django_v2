from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'id']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 20
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'category', 
        'price', 
        'orders_count', 
        'is_available', 
        'created_at', 
        'is_new_display'
    ]
    list_filter = [
        'category',
        'is_available', 
        'created_at'
    ]
    search_fields = [
        'name', 
        'description',
        'category__name'
    ]
    list_editable = [
        'price', 
        'orders_count', 
        'is_available'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at'
    ]
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('orders_count', 'is_available')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_new_display(self, obj):
        return obj.is_new
    is_new_display.boolean = True
    is_new_display.short_description = 'Новый товар'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')