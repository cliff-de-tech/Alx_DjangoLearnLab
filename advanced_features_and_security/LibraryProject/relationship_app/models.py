from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

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


# Role choices for UserProfile
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
]


class UserProfile(models.Model):
    """Model representing a user profile with role-based access control."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Signal to automatically create UserProfile when a new User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
