from mini_avito_app import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        lookup_field = "id"
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        lookup_field = "id"
        fields = ('id', 'user', 'address', 'full_name', 'phone', 'mail')


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        lookup_field = 'id'
        fields = ('id', 'p_cat', 'name', 'available', 'description', 'quantity', 'price', 'client')


class CategoryProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryProducts
        lookup_field = "id"
        fields = ('id', 'cp_name')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        lookup_field = "id"
        fields = ('id', 'status', 'price', 'client', 'product', 'quantity', 'delivery_status')
