from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Migrate existing products to have categories'
    
    def handle(self, *args, **options):
        # Создаем категорию по умолчанию
        default_category, created = Category.objects.get_or_create(
            name='Общая категория',
            defaults={'name': 'Общая категория'}
        )
        
        # Назначаем категорию всем существующим товарам
        products_without_category = Product.objects.filter(category__isnull=True)
        count = products_without_category.update(category=default_category)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned category to {count} products')
        )