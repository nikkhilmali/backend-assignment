from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.http import FileResponse, JsonResponse


import requests
# from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def upload_to_drive(request):
    access_token = request.headers.get("access-token")

    if not access_token:
        return Response({"error": "Access token is required"}, status=400)

    file = request.FILES["file"]

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = Credentials(access_token, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)

    file_metadata = {'name':file.name}
    media = MediaIoBaseUpload(file, mimetype=file.content_type)
    drive_service.files().create(body=file_metadata, media_body=media).execute()

    return Response({"message":"File Uploaded Successfully"})


@api_view(['GET'])
def list_drive_files(request):
    access_token = request.headers.get("access-token")

    if not access_token:
        return Response({"error": "Access token is required"}, status=400)
    
    creds = Credentials(access_token)
    drive_service = build("drive", "v3", credentials=creds)

    results = drive_service.files().list().execute()
    return Response(results.get("files", []))


@api_view(['GET'])
def download_drive_file(request):
    access_token = request.headers.get("access-token")
    file_id = request.query_params.get("file_id")

    if not access_token or not file_id:
        return JsonResponse(
            {"error": "Access token and file ID are required"}, status=400
        )

    # Build the Google Drive API service
    creds = Credentials(access_token)  # Extract Bearer token
    drive_service = build("drive", "v3", credentials=creds)

    # Get file metadata to retrieve file name and MIME type
    try:
        file_metadata = (
            drive_service.files().get(fileId=file_id, fields="name, mimeType").execute()
        )
        file_name = file_metadata.get("name", "downloaded_file")
        mime_type = file_metadata.get("mimeType", "application/octet-stream")
    except Exception as e:
        return JsonResponse(
            {"error": f"Failed to fetch file metadata: {str(e)}"}, status=400
        )

    # Download the file content
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        return FileResponse(
            response.raw, as_attachment=True, filename=file_name, content_type=mime_type
        )
    else:
        return JsonResponse(
            {"error": "Failed to download file"}, status=response.status_code
        )
