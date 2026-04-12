from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL слаг")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        # Если slug не передан (пустая строка) — генерируем из name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})