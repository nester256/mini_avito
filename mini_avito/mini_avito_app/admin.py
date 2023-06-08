from django.contrib import admin
from .models import *


class ProductsInline(admin.TabularInline):
    model = Products
    extra = 1


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


class Category_productsInline(admin.TabularInline):
    model = Category_products
    extra = 1


class Images_productsInline(admin.TabularInline):
    model = Images_products
    extra = 1


# Покупатель/Продавец
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [ProductsInline, OrderInline]
    list_filter = (
        'full_name',
    )


# Продукт
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    model = Products
    inlines = [Images_productsInline]
    list_filter = (
        'name',
        'available',
        'price',
    )


# Категория продуктов
@admin.register(Category_products)
class Category_productsAdmin(admin.ModelAdmin):
    model = Category_products
    list_filter = (
        'cp_name',
    )


# Заказ
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_filter = (
        'status',
        'price',
    )


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    model = Images
