from django.db import models


# Author model represents a book author.
# Each author can have multiple books (one-to-many relationship with Book).
class Author(models.Model):
    """
    Stores author information.
    Related to :model:`api.Book` via a one-to-many foreign key relationship.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Book model represents a published book.
# Each book is linked to exactly one Author via a ForeignKey.
class Book(models.Model):
    """
    Stores book information, related to :model:`api.Author`.
    - title: The title of the book.
    - publication_year: The year the book was published.
    - author: ForeignKey to Author — establishes a one-to-many relationship
      so that one author can have many books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
