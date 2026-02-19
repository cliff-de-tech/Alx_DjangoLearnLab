# Social Media API

A RESTful Social Media API built with Django and Django REST Framework.

---

## Setup

### Requirements

- Python 3.10+
- Django 6.x
- djangorestframework
- Pillow

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd social_media_api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework Pillow

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

---

## User Model

The custom user model (`accounts.CustomUser`) extends Django's `AbstractUser` with the following additional fields:

| Field             | Type             | Description                                                  |
|-------------------|------------------|--------------------------------------------------------------|
| `bio`             | TextField        | A short biography for the user (optional)                    |
| `profile_picture` | ImageField       | Profile picture, uploaded to `profile_pictures/` (optional)  |
| `followers`       | ManyToManyField  | Self-referential M2M (symmetrical=False); users who follow this user |

---

## Authentication

The API uses **token-based authentication** (via `rest_framework.authtoken`). Include the token in request headers:

```
Authorization: Token <your-token>
```

---

## API Endpoints

### Base URL: `/api/accounts/`

### 1. Register a New User

**POST** `/api/accounts/register/`

Request Body:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "bio": "Hello, I'm John!"
}
```

Response (`201 Created`):
```json
{
  "token": "abc123tokenvalue",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null
  }
}
```

---

### 2. Login

**POST** `/api/accounts/login/`

Request Body:
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

Response (`200 OK`):
```json
{
  "token": "abc123tokenvalue",
  "user_id": 1,
  "username": "john_doe"
}
```

---

### 3. View / Update Profile

**GET** `/api/accounts/profile/`  
**PUT / PATCH** `/api/accounts/profile/`

> Requires Authentication: `Authorization: Token <your-token>`

GET Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "Hello, I'm John!",
  "profile_picture": null,
  "followers_count": 0,
  "following_count": 0
}
```

PATCH Request Body (partial update):
```json
{
  "bio": "Updated bio text"
}
```

---

## Admin

Access the Django admin panel at `/admin/` to manage users and tokens.

Run the following to create a superuser:

```bash
python manage.py createsuperuser
```
