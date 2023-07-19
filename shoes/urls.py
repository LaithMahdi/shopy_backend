from django.urls import path
from .views import *
urlpatterns = [
    path('categorylist', CategoryListView.as_view()),
    path('categorylist/<int:pk>', CategoryDetailView.as_view()),
    path('shoeslist', ShoesListView.as_view()),
    path('shoeslist/<int:pk>', ShoesDetailView.as_view()),
     path('homepage', HomePageView.as_view()),
]