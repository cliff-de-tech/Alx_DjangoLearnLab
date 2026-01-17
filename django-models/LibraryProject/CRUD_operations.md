# CRUD Operations Documentation

This document contains all the CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django's ORM via the Django shell.

## 1. Create Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

### Expected Output
```python
# The book object is created and saved to the database
# <Book: 1984>
```

---

## 2. Retrieve Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

### Expected Output
```python
# Title: 1984, Author: George Orwell, Year: 1949
```

---

## 3. Update Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated Title: {book.title}")
```

### Expected Output
```python
# Updated Title: Nineteen Eighty-Four
```

---

## 4. Delete Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Confirm deletion
all_books = Book.objects.all()
print(f"All books: {all_books}")
```

### Expected Output
```python
# (1, {'bookshelf.Book': 1})
# All books: <QuerySet []>
```

---

## Summary

All CRUD operations have been successfully documented. You can test these operations by running the Django shell:

```bash
python manage.py shell
```

Then execute each command in sequence to see the operations in action.
