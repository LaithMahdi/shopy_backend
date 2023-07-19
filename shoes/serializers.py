from rest_framework import serializers
from .models import Category, Shoes

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShoesSerializer(serializers.ModelSerializer):
    category = CategorySerializer() 
    class Meta:
        model = Shoes
        fields = '__all__'
