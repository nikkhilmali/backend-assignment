from django.urls import path
from .views.oauth import google_login, google_callback
from .views.file_picker import upload_to_drive, list_drive_files, download_drive_file

urlpatterns = [
    path("auth/google/login/", google_login, name="google_login"),
    path("auth/google/callback/", google_callback, name="google_callback"),
    path("drive/upload/", upload_to_drive, name="upload_to_drive"),
    path("drive/list/", list_drive_files, name="list_drive_files"),
    path("drive/download/", download_drive_file, name="download_drive_file"),
]
