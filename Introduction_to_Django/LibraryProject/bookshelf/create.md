# Create Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

## Expected Output
```python
# The book object is created and saved to the database
# <Book: 1984>
```
