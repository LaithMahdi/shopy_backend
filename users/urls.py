from django.urls import path
from .views import *
urlpatterns = [
    path('register',SignUpView.as_view()),
    path('login',SignInView.as_view()),
    path('user',GetUserView.as_view()),
    path('logout',LogoutView.as_view()),
    path('sendverifycode',SendVerifyCodeView.as_view()),
    path('checkverifycode',CheckVerifyCodeView.as_view()),
    path('restpassword',RestPasswordView.as_view()),
]