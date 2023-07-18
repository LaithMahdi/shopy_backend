from django.urls import path
from .views import *
urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout',LogoutView.as_view()),
    path('sendverifycode',SendVerifyCodeView.as_view()),
    path('checkverifycode',CheckVerifyCodeView.as_view()),
    path('restpassword',RestPasswordView.as_view()),
]