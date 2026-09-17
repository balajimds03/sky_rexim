from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError,InvalidToken
from rest_framework.response import Response

class Authenticate(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None
        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token),validated_token
        except(TokenError,InvalidToken):
            response = Response({"error": "Access token invalid or expired"}, status=401)
            response.delete_cookie("access_token")
            return None
