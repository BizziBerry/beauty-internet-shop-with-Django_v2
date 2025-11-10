from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create test data for beauty shop'
    
    def handle(self, *args, **options):
        # Создаем категории для бьюти-товаров
        categories = [
            'Уход за кожей',
            'Декоративная косметика', 
            'Волосы',
            'Парфюмерия',
            'Маникюр и педикюр',
            'Бритье и эпиляция',
            'Аксессуары и инструменты'
        ]
        
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        
        # Создаем бьюти-товары
        products_data = [
            # Уход за кожей
            {'name': 'Очищающий гель для умывания', 'price': 1299, 'category': 'Уход за кожей', 'orders_count': 180, 'description': 'Нежный гель для ежедневного очищения кожи лица'},
            {'name': 'Увлажняющий крем для лица', 'price': 2499, 'category': 'Уход за кожей', 'orders_count': 150, 'description': 'Питательный крем с гиалуроновой кислотой'},
            {'name': 'Сыворотка с витамином C', 'price': 3599, 'category': 'Уход за кожей', 'orders_count': 95, 'description': 'Антивозрастная сыворотка для сияния кожи'},
            {'name': 'Патчи под глаза', 'price': 799, 'category': 'Уход за кожей', 'orders_count': 120, 'description': 'Гидрогелевые патчи против темных кругов'},
            
            # Декоративная косметика
            {'name': 'Тональный крем', 'price': 1899, 'category': 'Декоративная косметика', 'orders_count': 200, 'description': 'Легкий тональный крем с натуральным покрытием'},
            {'name': 'Палетка теней для век', 'price': 2799, 'category': 'Декоративная косметика', 'orders_count': 130, 'description': 'Палетка из 12 нейтральных оттенков'},
            {'name': 'Жидкая помада', 'price': 1499, 'category': 'Декоративная косметика', 'orders_count': 170, 'description': 'Стойкая матовая жидкая помада'},
            {'name': 'Тушь для ресниц', 'price': 1299, 'category': 'Декоративная косметика', 'orders_count': 220, 'description': 'Объемная тушь с эффектом накладных ресниц'},
            
            # Волосы
            {'name': 'Шампунь для объема', 'price': 1599, 'category': 'Волосы', 'orders_count': 140, 'description': 'Шампунь для придания объема тонким волосам'},
            {'name': 'Кондиционер-бальзам', 'price': 1699, 'category': 'Волосы', 'orders_count': 130, 'description': 'Восстанавливающий кондиционер для поврежденных волос'},
            {'name': 'Масло для кончиков волос', 'price': 2199, 'category': 'Волосы', 'orders_count': 85, 'description': 'Аргановое масло для блеска и питания'},
            {'name': 'Сухой шампунь', 'price': 999, 'category': 'Волосы', 'orders_count': 160, 'description': 'Экспресс-очищение волос без воды'},
            
            # Парфюмерия
            {'name': 'Цветочный парфюм 50ml', 'price': 4599, 'category': 'Парфюмерия', 'orders_count': 75, 'description': 'Нежный цветочный аромат с нотками жасмина'},
            {'name': 'Восточный парфюм 30ml', 'price': 3899, 'category': 'Парфюмерия', 'orders_count': 60, 'description': 'Стойкий восточный аромат с амброй'},
            {'name': 'Цитрусовые духи 100ml', 'price': 5299, 'category': 'Парфюмерия', 'orders_count': 45, 'description': 'Свежий цитрусовый аромат для ежедневного использования'},
            
            # Маникюр и педикюр
            {'name': 'Лак для ногтей', 'price': 499, 'category': 'Маникюр и педикюр', 'orders_count': 190, 'description': 'Стойкий лак для ногтей с глянцевым финишем'},
            {'name': 'База под лак', 'price': 699, 'category': 'Маникюр и педикюр', 'orders_count': 110, 'description': 'Укрепляющая база для продления стойкости маникюра'},
            {'name': 'Гель-лак набор', 'price': 3299, 'category': 'Маникюр и педикюр', 'orders_count': 70, 'description': 'Набор из 6 цветов гель-лака'},
            
            # Бритье и эпиляция
            {'name': 'Крем для депиляции', 'price': 1499, 'category': 'Бритье и эпиляция', 'orders_count': 90, 'description': 'Нежный крем для депиляции с алоэ вера'},
            {'name': 'Бритвенный станок', 'price': 799, 'category': 'Бритье и эпиляция', 'orders_count': 150, 'description': 'Многоразовый бритвенный станок с 5 лезвиями'},
            {'name': 'Воск для эпиляции', 'price': 1899, 'category': 'Бритье и эпиляция', 'orders_count': 65, 'description': 'Натуральный воск для домашней эпиляции'},
            
            # Аксессуары и инструменты
            {'name': 'Кисти для макияжа набор', 'price': 2799, 'category': 'Аксессуары и инструменты', 'orders_count': 95, 'description': 'Профессиональный набор из 8 кистей'},
            {'name': 'Зеркало с подсветкой', 'price': 3299, 'category': 'Аксессуары и инструменты', 'orders_count': 55, 'description': 'Косметическое зеркало с LED-подсветкой'},
            {'name': 'Фен мощный 2000Вт', 'price': 4299, 'category': 'Аксессуары и инструменты', 'orders_count': 80, 'description': 'Профессиональный фен с ионизацией'},
        ]
        
        # Создаем товары с разными датами для тестирования фильтра по дате
        for i, product_data in enumerate(products_data):
            category = Category.objects.get(name=product_data['category'])
            
            # Создаем товары с разными датами добавления
            if i < 8:  # Первые 8 товаров - очень новые (последние 3 дня)
                created_date = timezone.now() - timedelta(days=random.randint(0, 3))
            elif i < 16:  # Следующие 8 - новые (4-10 дней назад)
                created_date = timezone.now() - timedelta(days=random.randint(4, 10))
            elif i < 20:  # Следующие 4 - не новые (2-3 недели назад)
                created_date = timezone.now() - timedelta(days=random.randint(14, 21))
            else:  # Остальные - старые (больше месяца)
                created_date = timezone.now() - timedelta(days=random.randint(35, 60))
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': product_data['price'],
                    'category': category,
                    'orders_count': product_data['orders_count'],
                    'description': product_data['description'],
                    'is_available': True,
                    'created_at': created_date
                }
            )
            
            if created:
                self.stdout.write(f'Создан: {product.name} - {product.price} руб.')
            else:
                self.stdout.write(f'Уже существует: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные для бьюти-магазина успешно созданы!'))
        self.stdout.write(self.style.SUCCESS(f'📦 Создано товаров: {len(products_data)}'))
        self.stdout.write(self.style.SUCCESS(f'📁 Создано категорий: {len(categories)}'))