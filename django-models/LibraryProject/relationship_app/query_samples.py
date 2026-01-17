"""
Query samples demonstrating different Django ORM relationship queries.

This script demonstrates how to query:
1. ForeignKey relationships (Book -> Author)
2. ManyToMany relationships (Library -> Books)
3. OneToOne relationships (Librarian -> Library)

To run these queries, use the Django shell:
    python manage.py shell
    >>> exec(open('relationship_app/query_samples.py').read())
"""

import django
import os

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# Query all books by a specific author using ForeignKey relationship
def get_books_by_author(author_name):
    """
    Query all books written by a specific author.
    Uses the ForeignKey relationship from Book to Author.
    """
    try:
        author = Author.objects.get(name=author_name)
        # Using the related_name 'books' defined in the Book model
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None


# List all books in a library using ManyToMany relationship
def get_books_in_library(library_name):
    """
    Query all books available in a specific library.
    Uses the ManyToMany relationship from Library to Book.
    """
    try:
        library = Library.objects.get(name=library_name)
        # Access the many-to-many relationship
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


# Retrieve the librarian for a library using OneToOne relationship
def get_librarian_for_library(library_name):
    """
    Query the librarian assigned to a specific library.
    Uses the OneToOne relationship from Librarian to Library.
    """
    try:
        library = Library.objects.get(name=library_name)
        # Access the reverse OneToOne relationship using the related_name
        librarian = Librarian.objects.get(library=library)
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None


# Example usage (uncomment to test in Django shell)
if __name__ == "__main__":
    print("Query Samples for Relationship App")
    print("=" * 40)
    
    # These examples assume you have created test data
    # You can create test data using Django admin or shell:
    #
    # >>> from relationship_app.models import Author, Book, Library, Librarian
    # >>> author = Author.objects.create(name="J.K. Rowling")
    # >>> book = Book.objects.create(title="Harry Potter", author=author)
    # >>> library = Library.objects.create(name="City Library")
    # >>> library.books.add(book)
    # >>> librarian = Librarian.objects.create(name="John Smith", library=library)
    
    print("\n1. Query all books by a specific author:")
    print("   books = get_books_by_author('Author Name')")
    
    print("\n2. List all books in a library:")
    print("   books = get_books_in_library('Library Name')")
    
    print("\n3. Retrieve the librarian for a library:")
    print("   librarian = get_librarian_for_library('Library Name')")
