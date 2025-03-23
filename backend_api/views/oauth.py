import requests
# from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend_core import settings
from ..constants import Constants


@api_view(['GET'])
def google_login(request):
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/drive.file",
    }

    auth_url = f"{Constants().GOOGLE_AUTH_URL}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}&scope={params['scope']}"

    return redirect(auth_url)


@api_view(['GET'])
def google_callback(request):
    code = request.GET.get('code')

    if not code:
        return Response({"error": "Authorization code not provided"}, status=400)
    
    data = {
        "code":code, 
        "client_id" : settings.GOOGLE_CLIENT_ID,
        "client_secret":settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri":settings.REDIRECT_URI,
        "grant_type":"authorization_code",
    }

    response = requests.post(url=Constants.GOOGLE_TOKEN_URL, data=data, timeout=5).json()

    access_token = response.get("access_token")
    print("access_token", access_token, flush=True)


    user_info = requests.get(url=Constants.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}, timeout=5).json()

    return Response(data={"user_info":user_info, "access_token":access_token})
