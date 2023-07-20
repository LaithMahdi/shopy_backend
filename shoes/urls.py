from django.urls import path
from .views import *
urlpatterns = [
    path('categorylist', CategoryListView.as_view()),
    path('categorylist/<int:pk>', CategoryDetailView.as_view()),
    path('shoeslist', ShoesListView.as_view()),
    path('shoeslist/<int:pk>', ShoesDetailView.as_view()),
    path('homepage', HomePageView.as_view()),
    path('category/<int:category_id>', ShoesByCategoryView.as_view()),
    path('search/', ShoesSearchView.as_view()),
    path('order/', ShoesOrderView.as_view()),
]   