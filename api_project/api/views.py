from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    Uses ListAPIView for read-only access to the book collection.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update`, `partial_update`, and `destroy` actions.
    
    Authentication and Permissions:
    - Token authentication is required for all operations.
    - Only authenticated users can access these endpoints.
    - Use the token obtained from /api-token-auth/ in the Authorization header.
    - Header format: Authorization: Token <your_token>
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]