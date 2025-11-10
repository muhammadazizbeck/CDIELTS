# views.py
import requests
import jwt
from jwt import PyJWKClient
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleAuthRedirect(APIView):
    def get(self, request):
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope=openid%20email%20profile"
            f"&access_type=offline"
            f"&prompt=consent"
        )
        return Response({"auth_url": auth_url})

class GoogleCallback(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Kod topilmadi"}, status=400)

        # 1. Token olish
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_r = requests.post(token_url, data=token_data)
        if token_r.status_code != 200:
            return Response({"error": "Token olishda xato"}, status=400)

        id_token = token_r.json().get("id_token")
        if not id_token:
            return Response({"error": "ID token topilmadi"}, status=400)

        # 2. ID Tokenni tekshirish
        try:
            jwks_client = PyJWKClient("https://www.googleapis.com/oauth2/v3/certs")
            signing_key = jwks_client.get_signing_key_from_jwt(id_token)
            payload = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.GOOGLE_CLIENT_ID,
            )
        except Exception as e:
            return Response({"error": "Token xato", "detail": str(e)}, status=400)

        # 3. Foydalanuvchi ma'lumotlari
        email = payload.get("email")
        if not email or not payload.get("email_verified"):
            return Response({"error": "Email tasdiqlanmagan"}, status=400)

        # 4. User yaratish yoki olish
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": payload.get("given_name", ""),
                "last_name": payload.get("family_name", ""),
            }
        )
        if created:
            user.set_unusable_password()
            user.save()

        # 5. JWT berish
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name() or user.username,
            }
        })