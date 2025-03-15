from django.urls import path
from .views import google_login, google_callback

urlpatterns = [
    path('auth/google/login/', google_login, name='google_login'),
    path('auth/google/callback/', google_callback, name='google_callback'),
]
