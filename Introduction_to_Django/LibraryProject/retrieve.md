# Retrieve Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

## Expected Output
```python
# Title: 1984, Author: George Orwell, Year: 1949
```
