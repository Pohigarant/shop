from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from products.models import Product
from users.models import User


# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Товар",
    )
    user = models.ForeignKey(
        User,
        related_name="user_reviews",
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )  # например от 1 до 5
    text = models.TextField(verbose_name="Текст отзыва")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            UniqueConstraint(
                fields=["user", "product"], name="unique_employee_fullname"
            ),
        )

    def __str__(self):
        return f"Отзыв от {self.user.username}"
