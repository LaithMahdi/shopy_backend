from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Category, Shoes,Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShoesSerializer(serializers.ModelSerializer):
    category = CategorySerializer() 
    class Meta:
        model = Shoes
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
