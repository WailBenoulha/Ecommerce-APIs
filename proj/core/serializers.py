from rest_framework import serializers
from core import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'name', 'created_by', 'price', 'image', 'category_prod')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'description')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Order
        fields=('id','date','order_by','product')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','role','email','name','last_name','address','phone_number')         