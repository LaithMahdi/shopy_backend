from rest_framework import generics
from django.shortcuts import get_object_or_404
import shoes
from .models import Category, Shoes,Favorite
from .serializers import CategorySerializer, ShoesSerializer,FavoriteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q,F

# View for getting all categories and creating a new category
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View for getting a single category by its ID, updating and deleting a category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View for getting all shoes and creating a new shoe
class ShoesListView(generics.ListCreateAPIView):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer

# View for getting a single shoe by its ID, updating and deleting a shoe
class ShoesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer


class HomePageView(APIView):
    def get(self, request, format=None):
        # Get all categories
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        # Get shoes with discount > 0
        shoes_with_discount = Shoes.objects.filter(shoes_discount__gt=0)
        shoes_serializer = ShoesSerializer(shoes_with_discount, many=True)

        # Combine the results into a single response
        response_data = {
            'message': 'success',
            'categories': categories_serializer.data,
            'shoes_with_discount': shoes_serializer.data
        }
        return Response(response_data)
    
class ShoesByCategoryView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            shoes = Shoes.objects.filter(category=category)
            serializer = ShoesSerializer(shoes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ShoesSearchView(APIView):
    def get(self, request):
        search_query = request.query_params.get('search')
        if not search_query:
            return Response({"error": "Search query parameter 'search' is required."}, status=status.HTTP_400_BAD_REQUEST)

        shoes = Shoes.objects.filter(
            Q(shoes_name__icontains=search_query) | Q(shoes_name_ar__icontains=search_query)
        )
        serializer = ShoesSerializer(shoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ShoesOrderView(APIView):
    def get(self, request):
        order_by = request.query_params.get('order_by')
        if not order_by or order_by not in ['low_to_high', 'high_to_low']:
            return Response({"error": "Invalid or missing 'order_by' parameter. Use 'low_to_high' or 'high_to_low'."}, status=status.HTTP_400_BAD_REQUEST)

        if order_by == 'low_to_high':
            shoes = Shoes.objects.all().order_by('shoes_price')
        else:
            shoes = Shoes.objects.all().order_by(F('shoes_price').desc())

        serializer = ShoesSerializer(shoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    




    

