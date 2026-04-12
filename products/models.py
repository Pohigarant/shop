from django.urls import reverse
from django.db import models
from slugify import slugify

from categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='products',
                                 verbose_name="Категория",
                                 null=True, blank=True)

    name = models.CharField(max_length=255, verbose_name="Имя")
    model = models.CharField(max_length=255, verbose_name="Модель", blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL слаг")
    article = models.CharField(max_length=50, verbose_name="Артикул", blank=True)
    product_info = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество товара")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.pk:
            old = Product.objects.get(pk=self.pk)
            if old.name != self.name:
                self.slug = slugify(self.name)
        else:
            if not self.slug:
                self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
