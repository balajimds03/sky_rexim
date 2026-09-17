from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework.permissions import AllowAny
from utils import Cookies
from django.conf import settings
# Create your views here.

class Register(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serial = UserSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response({"message":"Account Registered Successfully"},status=200)
        return Response(serial.errors,status=400)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            response = Response({"message":"Login Successfull"},status=200)
            Cookies.set_secure_cookies(response,"refresh_token",str(refresh_token),60*60*24*7)
            Cookies.set_secure_cookies(response,"access_token",str(access_token),60*15)
            return response 
        return Response({"error":"Invalid Credentials"},status=401)

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        old_token = request.COOKIES.get("refresh_token")
        if old_token:
            try:
                token = RefreshToken(old_token)
                user_id = token.payload.get("user_id")
                user = User.objects.get(pk=user_id)
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                token.blacklist()
                response = Response({"message":"Tokens Updated"},status=200)
                Cookies.set_secure_cookies(response,"refresh_token",str(refresh_token),60*24*7)
                Cookies.set_secure_cookies(response,"access_token",str(access_token),60*60*15)
                return response 
            except(InvalidToken,TokenError):
                return Response({"error":"Token Invalid or Expired"},status=400)
        return Response({"error":"Token not found"},status=404)
    
class Logout(APIView):
    def post(self,request):
        response = Response({"message":"Successfully Logout"})
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response
    
class ChangePassword(APIView):
    def post(self,request):
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")
        if new_password != confirm_new_password:
            return Response({"error":"Password is missmatch"},status=400)
        user = request.user
        if not user.check_password(password):
            return Response({"error":"Password is wrong"},status=400)
        user.set_password(new_password)
        user.save()
        return Response({"message":"Password Updated Successfully"},status=200)
        
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

class ForgotPasswordRequest(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        email = request.data.get("email")
        if not email:
            return Response({"error":"Email is required"},status=404)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"Invalid email"},status=400)
            
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/auth/password-reset/{uid}/{token}"
        subject = "Password Reset Request"
        from_email = settings.EMAIL_HOST_USER
        to = [email]
        html_content = render_to_string("emails/PasswordReset.html",{"reset_link":reset_link})
        text_content = strip_tags(html_content)
        mail = EmailMultiAlternatives(subject=subject,body=text_content,from_email=from_email,to=to)
        mail.attach_alternative(html_content,"text/html")
        mail.send()
        return Response({"message":"Password reset email sent to your mail"},status=200)
        
class PasswordReset(APIView):
    def post(self,request,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user and default_token_generator.check_token(user,token):
            password = request.data.get("password")
            confirm_password = request.data.get("confirm_password")
            if password != confirm_password:
                return Response({"error":"Passwords miss match"},status=400)
            user.set_password(password)
            user.save()
            return Response({"message":"Password Updated"},status=200)
        return Response({"error":"Invlid or Expired Token"})