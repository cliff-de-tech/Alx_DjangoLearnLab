from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer


# ListView: Retrieves all books. Open to all users (read-only for unauthenticated).
# Supports filtering by title, author, and publication_year via DjangoFilterBackend.
# Supports text search on title and author name via SearchFilter.
# Supports ordering by title and publication_year via OrderingFilter.
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of all Book instances.
    Accessible to all users; unauthenticated users get read-only access.

    Filtering:
        ?title=<value>           - Filter by exact title
        ?author=<id>             - Filter by author ID
        ?publication_year=<year> - Filter by publication year

    Searching:
        ?search=<term>           - Search across title and author name

    Ordering:
        ?ordering=title          - Order by title (ascending)
        ?ordering=-title         - Order by title (descending)
        ?ordering=publication_year - Order by publication year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, and ordering backends
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # DjangoFilterBackend: fields available for exact-match filtering
    filterset_fields = ['title', 'author', 'publication_year']

    # SearchFilter: fields available for text search
    search_fields = ['title', 'author__name']

    # OrderingFilter: fields available for ordering; default ordering by title
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


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
