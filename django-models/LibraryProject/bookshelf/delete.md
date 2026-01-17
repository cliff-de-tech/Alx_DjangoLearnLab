# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Confirm deletion
all_books = Book.objects.all()
print(f"All books: {all_books}")
```

## Expected Output
```python
# (1, {'bookshelf.Book': 1})
# All books: <QuerySet []>
```
