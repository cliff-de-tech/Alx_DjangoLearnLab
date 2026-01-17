from django.db import models

# Create your models here.


class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book with a ForeignKey relationship to Author."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Library(models.Model):
    """Model representing a library with a ManyToMany relationship to Book."""
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Model representing a librarian with a OneToOne relationship to Library."""
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name
