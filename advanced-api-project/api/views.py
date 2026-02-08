from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


# ListView: Retrieves all books. Open to all users (read-only for unauthenticated).
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of all Book instances.
    Accessible to all users; unauthenticated users get read-only access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# DetailView: Retrieves a single book by its primary key.
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/
    Returns a single Book instance identified by its primary key.
    Accessible to all users; unauthenticated users get read-only access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CreateView: Allows authenticated users to add a new book.
# Performs data validation through the serializer (including custom
# publication_year validation defined in BookSerializer).
class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Creates a new Book instance.
    Restricted to authenticated users only.
    The serializer handles validation, including ensuring
    publication_year is not in the future.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# UpdateView: Allows authenticated users to modify an existing book.
# Handles both PUT (full update) and PATCH (partial update) requests.
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<int:pk>/update/
    Updates an existing Book instance.
    Restricted to authenticated users only.
    Supports both full and partial updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# DeleteView: Allows authenticated users to remove a book.
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/
    Deletes an existing Book instance.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
