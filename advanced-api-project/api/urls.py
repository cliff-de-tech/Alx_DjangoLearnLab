from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    # Retrieve a single book by primary key
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # Create a new book (authenticated users only)
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    # Update an existing book (authenticated users only)
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    # Delete a book (authenticated users only)
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
