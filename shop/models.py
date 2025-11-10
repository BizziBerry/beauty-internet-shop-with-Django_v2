from django.db import models
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )
    description = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория товара',
        related_name='products'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение товара',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    orders_count = models.IntegerField(
        default=0,
        verbose_name='Количество заказов'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен для заказа'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    @property
    def is_new(self):
        """Товар считается новым, если добавлен в последние 7 дней"""
        return self.created_at >= timezone.now() - timedelta(days=7)
    
    def get_price_range_display(self):
        """Метод для отображения ценового диапазона"""
        if self.price < 1000:
            return "Бюджетный"
        elif self.price < 5000:
            return "Средний"
        else:
            return "Премиум"