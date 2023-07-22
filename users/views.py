from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
import jwt,datetime
from django.core.mail import send_mail, BadHeaderError
from rest_framework_simplejwt.tokens import AccessToken
import random
import string
from django.conf import settings

# Create your views here.


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Successfully signed up!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            # User exists, now check the password
            if user.check_password(password):
                return Response({'token': self.get_access_token(user)})
            else:
                return Response({'error': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_access_token(self, user):
        access_token = AccessToken.for_user(user)
        return str(access_token)

class LogoutView(APIView):
    def post(self, request):
        # Your logout code here, without the need to invalidate refresh tokens
        return Response(status=status.HTTP_205_RESET_CONTENT)

class GetUserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class SendVerifyCodeView(APIView):
    def post(self, request):
        email = request.data['email']
        subject = 'Verify code Shopy App'
        verification_code = ''.join(random.choices(string.digits, k=6))
        message = f'Your verification code is: {verification_code}'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the verification code in the user's verification_code field
        try:
            user = User.objects.get(email=email)
            user.verification_code = verification_code
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)
    
class CheckVerifyCodeView(APIView):
    def post(self, request):
        email = request.data['email']
        verify_code = request.data['verify_code']

        try:
            user = User.objects.get(email=email)
            if user.verification_code == verify_code:
                # Verification code matches
                return Response({'message': 'Verification code is valid.'}, status=status.HTTP_200_OK)
            else:
                # Verification code does not match
                return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        # User not found or other exception occurred
        return Response({'error': 'Verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
    
class RestPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)



