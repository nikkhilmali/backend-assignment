# Backend API with OAuth, Google Drive, and WebSockets

This Django backend API integrates Google OAuth 2.0 for authentication, Google Drive API for file management, and WebSockets for real-time chat functionality.

## 🚀 Features

- **Google OAuth 2.0:** Secure user authentication
- **Google Drive Integration:** Upload, list, and download files
- **Real-time WebSocket Chat:** Instant messaging between users

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account with OAuth 2.0 credentials
- Google Drive API enabled

## 🔧 Setup & Installation

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```
   DEBUG=True
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   REDIRECT_URI=http://localhost:8000/api/auth/google/callback/
   ```

5. **Run migrations**
   ```
   python manage.py migrate
   ```

## 🏃‍♂️ Running the Application

The application requires two concurrent processes:

1. **Run the Django server**
   ```
   python manage.py runserver
   ```

2. **Run the WebSocket server with Daphne**
   ```
   daphne -b 0.0.0.0 -p 8001 backend_api.asgi:application
   ```

### Running both servers concurrently

#### Option 1: Using background processes
```
python manage.py runserver & daphne -b 0.0.0.0 -p 8001 backend_api.asgi:application
```

#### Option 2: Create a shell script (start.sh)
```bash
#!/bin/bash
python manage.py migrate
python manage.py runserver &
daphne -b 0.0.0.0 -p 8001 backend_api.asgi:application
```

Make it executable: `chmod +x start.sh`
Run it: `./start.sh`

## 📝 API Endpoints

### Google OAuth Flow

1. **Initiate Google Auth Flow**
   - `GET /api/auth/google/login/`
   - Redirects to Google Auth page

2. **Google Auth Callback**
   - `GET /api/auth/google/callback/`
   - Receives authentication data from Google

### Google Drive Integration

3. **Upload File to Google Drive**
   - `POST /api/drive/upload/`
   - Headers: `access-token: <google-access-token>`
   - Body: Form data with file

4. **List Google Drive Files**
   - `GET /api/drive/list/`
   - Headers: `access-token: <google-access-token>`

5. **Download File from Google Drive**
   - `GET /api/drive/download/?file_id=<file-id>`
   - Headers: `access-token: <google-access-token>`

### WebSocket for Chat

- WebSocket URL: `ws://localhost:8001/ws/chat/`
- Message format:
  ```json
  {
    "message": "Your message here"
  }
  ```

## 📄 [Postman Collection](https://app.getpostman.com/join-team?invite_code=a1742535fb9c9d9a734fb99dad5d11553c74b848e485376d011378e4e01c67fa&target_code=16856f323b6fe65ea9d87b0171af9e15)
