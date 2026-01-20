from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book
from .forms import BookForm, ExampleForm

# Create your views here.

"""
Security Measures Implemented in Views:

1. SQL Injection Prevention:
   - All database queries use Django ORM, which automatically parameterizes queries
   - No raw SQL queries or string formatting is used
   - get_object_or_404() safely retrieves objects and handles invalid IDs

2. Input Validation:
   - All user input is validated through Django forms (BookForm)
   - Form validation includes field type checking and custom validators
   - Only valid, sanitized data is saved to the database

3. CSRF Protection:
   - All POST requests require CSRF tokens (enforced by Django middleware)
   - Forms include {% csrf_token %} in templates

4. Permission-based Access Control:
   - All views use @permission_required decorator
   - raise_exception=True ensures unauthorized users get 403 errors
   - Users must have specific permissions to access each view

5. Secure Object Retrieval:
   - get_object_or_404() prevents information leakage about non-existent objects
   - Returns 404 for invalid IDs instead of exposing database errors
"""

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books.
    Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {
        'form': form,
        'title': 'Create Book',
        'action': 'Create'
    })


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book.
    Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/form_example.html', {
        'form': form,
        'title': f'Edit Book: {book.title}',
        'action': 'Update'
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

