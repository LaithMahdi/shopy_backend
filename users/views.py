from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt,datetime
from django.core.mail import send_mail, BadHeaderError
import random
import string
from django.conf import settings

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload={
            'id':user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=2),
            'iat':datetime.datetime.utcnow()
        }
        token=jwt.encode(payload,'secret',algorithm='HS256')

        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }
        return response
    
class SendVerifyCode(APIView):
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
        return Response({'message': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)



