# Update Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated Title: {book.title}")
```

## Expected Output
```python
# Updated Title: Nineteen Eighty-Four
```
