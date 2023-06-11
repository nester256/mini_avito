from django.contrib import admin
from mini_avito_app import models


class ProductsInline(admin.TabularInline):
    model = models.Products
    extra = 1


class OrderInline(admin.TabularInline):
    model = models.Order
    extra = 1


class CategoryProductsInline(admin.TabularInline):
    model = models.CategoryProducts
    extra = 1


class ImagesProductsInline(admin.TabularInline):
    model = models.ImagesProducts
    extra = 1


# Покупатель/Продавец
@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    model = models.Client
    inlines = [ProductsInline, OrderInline]
    list_filter = (
        'full_name',
    )


# Продукт
@admin.register(models.Products)
class ProductsAdmin(admin.ModelAdmin):
    model = models.Products
    inlines = [ImagesProductsInline]
    list_filter = (
        'name',
        'available',
        'price',
    )


# Категория продуктов
@admin.register(models.CategoryProducts)
class CategoryProductsAdmin(admin.ModelAdmin):
    model = models.CategoryProducts
    list_filter = (
        'cp_name',
    )


# Заказ
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_filter = (
        'status',
        'price',
    )


@admin.register(models.Images)
class ImagesAdmin(admin.ModelAdmin):
    model = models.Images
