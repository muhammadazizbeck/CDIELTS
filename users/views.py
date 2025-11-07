import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from users.models import CustomUser

class GoogleAuthRedirect(APIView):
    def get(self,request):
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        client_id = settings.GOOGLE_CLIENT_ID
        scope = 'openid email profile'

        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
            f"&access_type=offline"
        )
        return Response({"auth_url":google_auth_url})

class GoogleAuthCallback(APIView):
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"error": "Code talab qilinadi"}, status=400)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        if token_response.status_code != 200:
            return Response({"error": "Google token olishda xato"}, status=400)

        access_token = token_response.json().get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get(user_info_url, headers=headers)
        if user_response.status_code != 200:
            return Response({"error": "Foydalanuvchi ma'lumotlarini olishda xato"}, status=400)

        user_data = user_response.json()
        email = user_data["email"]
        google_id = user_data["id"]
        name = user_data.get("name", "")
        picture = user_data.get("picture", "")

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": name.split()[0] if name else "",
                "last_name": " ".join(name.split()[1:]) if name else "",
                "is_verified": True,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        # JWT yaratish
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name(),
                "role": user.role,
            }
        })
    
