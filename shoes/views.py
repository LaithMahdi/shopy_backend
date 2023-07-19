from rest_framework import generics
from .models import Category, Shoes
from .serializers import CategorySerializer, ShoesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


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