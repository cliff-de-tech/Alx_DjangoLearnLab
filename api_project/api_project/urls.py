"""
URL configuration for api_project project.

Authentication:
- Token authentication is enabled for this API.
- To obtain a token, POST to /api-token-auth/ with username and password.
- Include the token in requests: Authorization: Token <your_token>
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
