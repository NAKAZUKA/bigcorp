import random
import string

from django.db import models
from django.urls import reverse
# from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Класс категории"""
    name = models.CharField(
        max_length=200, verbose_name='Название категории', db_index=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        editable=True,
        verbose_name='URL'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    class Meta:
        db_table = 'Category'
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    @staticmethod
    def _rand_slug():
        return ''.join(
            random.choice(
                string.ascii_lowercase + string.digits
                ) for _ in range(3)
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', args=[str(self.slug)])


class Product(models.Model):
    """Класс продукта"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название продукта'
    )
    brand = models.CharField(
        max_length=200,
        verbose_name='Бренд'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=200,
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Цена',
        default=99.99
    )
    image = models.ImageField(
        upload_to='products/products/%Y/%m/%d',
        verbose_name='Изображение',
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Наличие'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[str(self.slug)])


class ProductManager(models.Manager):
    """Класс для управления продуктами"""
    def get_queryset(self):
        return super(ProductManager, self).get_queryset(
        ).filter(available=True)


class ProductProxy(Product):
    """Класс для проксирования модели Product"""
    objects = ProductManager()

    class Mete:
        proxy = True
