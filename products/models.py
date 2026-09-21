from django.db import models
from django.urls import reverse
from slugify import slugify

from categories.models import Category


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(models.Model):
    objects = models.Manager()  # все товары — для админки
    available = ActiveProductManager()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255, verbose_name="Имя")
    model = models.CharField(max_length=255, verbose_name="Модель", blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name="URL слаг"
    )
    article = models.CharField(
        max_length=50, verbose_name="Артикул", blank=True
    )
    product_info = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Количество товара"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    average_rating = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    reviews_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("name",)
        constraints = (
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="product_price_non_negative",
            ),
        )
        indexes = (
            models.Index(fields=["is_active"]),
            models.Index(fields=["category", "is_active"]),
        )

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._old_name = instance.name
        return instance

    def _unique_slug(model, name, pk=None):
        base = slugify(name)
        slug, i = base, 2
        qs = model.objects.exclude(pk=pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug or self.name != getattr(self, "_old_name", None):
            self.slug = self._unique_slug(Product, self.name, self.pk)
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"slug"}
        super().save(*args, **kwargs)
        self._old_name = self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    @property
    def in_stock(self) -> bool:
        return self.is_active and self.quantity > 0
