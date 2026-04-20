from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Product


class ProductFilter(filters.FilterSet):
    # 1. Строковые фильтры
    name = filters.CharFilter(lookup_expr='icontains', label='Название (содержит)')
    model = filters.CharFilter(lookup_expr='icontains', label='Модель (содержит)')
    article = filters.CharFilter(lookup_expr='icontains', label='Артикул (содержит)')

    # 2. Универсальный поиск по трём полям
    search = filters.CharFilter(method='filter_search', label='Поиск (имя/модель/артикул)')

    # 3. Числовые фильтры для цены
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')

    # 4. Числовой фильтр для количества (например, остаток на складе)
    quantity_min = filters.NumberFilter(field_name='quantity', lookup_expr='gte', label='Количество от')
    quantity_max = filters.NumberFilter(field_name='quantity', lookup_expr='lte', label='Количество до')

    # 5. Булевы фильтры
    is_active = filters.BooleanFilter(label='Активен')
    in_stock = filters.BooleanFilter(method='filter_in_stock', label='В наличии')

    # 6. Фильтр по категории (через slug и через ID)
    category_slug = filters.CharFilter(field_name='category__slug', lookup_expr='exact', label='Категория (slug)')
    category_id = filters.NumberFilter(field_name='category__id', label='Категория (ID)')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='exact', label='Категория (имя)')

    # 7. Фильтры по датам
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Создан после')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Создан до')

    # 8. Сортировка (через OrderingFilter, но можно и через filter_backends)
    #ordering = filters.OrderingFilter(
        #fields=(
            #('price', 'price'),
            #('name', 'name'),
            #('created_at', 'created_at'),
            #('-created_at', '-created_at'),
        #),
        #label='Сортировка'
    #)

    class Meta:
        model = Product
        fields = []  # всё объявлено явно

    # ----- Кастомные методы -----
    def filter_search(self, queryset, name, value):
        """Поиск по имени, модели и артикулу"""
        return queryset.filter(
            Q(name__icontains=value) |
            Q(model__icontains=value) |
            Q(article__icontains=value)
        )

    def filter_in_stock(self, queryset, name, value):
        """Фильтр по наличию (quantity > 0)"""
        if value:
            return queryset.filter(quantity__gt=0)
        return queryset.filter(quantity=0)