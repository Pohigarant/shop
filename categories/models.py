from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name="URL слаг"
    )

    class Meta:
        verbose_name = ("Категория",)
        verbose_name_plural = ("Категории",)
        ordering = ("name",)

    def __str__(self):
        return self.name

    def _unique_slug(self):
        base = slugify(self.name)
        slug, i = base, 2
        qs = self.__class__.objects.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug or self.name != getattr(self, "_old_name", None):
            self.slug = self._unique_slug()
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"slug"}
        super().save(*args, **kwargs)
        self._old_name = self.name

    def get_absolute_url(self):
        return reverse("categories-detail", kwargs={"pk": self.pk})
