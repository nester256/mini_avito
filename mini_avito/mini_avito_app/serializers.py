from rest_framework import serializers
from .models import User, Client, Products, Category_products, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        lookup_field = "id"
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        lookup_field = "id"
        fields = ('id', 'user', 'address', 'full_name', 'phone', 'mail')


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        lookup_field = 'id'
        fields = ('id', 'p_cat', 'name', 'available', 'description', 'quantity', 'price', 'client')


class Category_productsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_products
        lookup_field = "id"
        fields = ('id', 'cp_name')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        lookup_field = "id"
        fields = ('id', 'status', 'price', 'client', 'product', 'quantity', 'delivery_status')
