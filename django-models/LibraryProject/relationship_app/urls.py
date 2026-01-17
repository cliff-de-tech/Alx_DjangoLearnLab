from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view: Library detail by primary key
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
