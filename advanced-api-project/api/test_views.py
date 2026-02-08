from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for the Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering,
    and permission/authentication enforcement.
    """

    def setUp(self):
        """
        Set up test data and clients.
        Creates a test user, an author, and sample books for use across tests.
        """
        # Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client = APIClient()

        # Create test author and books
        self.author = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')

        self.book1 = Book.objects.create(
            title='Harry Potter', publication_year=1997, author=self.author
        )
        self.book2 = Book.objects.create(
            title='1984', publication_year=1949, author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm', publication_year=1945, author=self.author2
        )

    # ------------------------------------------------------------------ #
    #  CRUD: CREATE
    # ------------------------------------------------------------------ #

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author.pk,
        }
        response = self.client.post(reverse('book-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Book')

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book."""
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author.pk,
        }
        response = self.client.post(reverse('book-create'), data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_book_future_year_rejected(self):
        """Test that a book with a future publication year is rejected."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Future Book',
            'publication_year': 2099,
            'author': self.author.pk,
        }
        response = self.client.post(reverse('book-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------ #
    #  CRUD: READ (List & Detail)
    # ------------------------------------------------------------------ #

    def test_list_books(self):
        """Test retrieving the list of all books."""
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_detail_book(self):
        """Test retrieving a single book by its primary key."""
        response = self.client.get(
            reverse('book-detail', kwargs={'pk': self.book1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')

    # ------------------------------------------------------------------ #
    #  CRUD: UPDATE
    # ------------------------------------------------------------------ #

    def test_update_book_authenticated(self):
        """Test that an authenticated user can update a book."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Harry Potter Updated',
            'publication_year': 1997,
            'author': self.author.pk,
        }
        response = self.client.put(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter Updated')

    def test_update_book_unauthenticated(self):
        """Test that an unauthenticated user cannot update a book."""
        data = {'title': 'Hacked Title'}
        response = self.client.put(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data,
            format='json',
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # ------------------------------------------------------------------ #
    #  CRUD: DELETE
    # ------------------------------------------------------------------ #

    def test_delete_book_authenticated(self):
        """Test that an authenticated user can delete a book."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(
            reverse('book-delete', kwargs={'pk': self.book1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete a book."""
        response = self.client.delete(
            reverse('book-delete', kwargs={'pk': self.book1.pk})
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # ------------------------------------------------------------------ #
    #  FILTERING
    # ------------------------------------------------------------------ #

    def test_filter_by_title(self):
        """Test filtering books by exact title."""
        response = self.client.get(reverse('book-list'), {'title': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_by_author(self):
        """Test filtering books by author ID."""
        response = self.client.get(
            reverse('book-list'), {'author': self.author2.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get(
            reverse('book-list'), {'publication_year': 1949}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    # ------------------------------------------------------------------ #
    #  SEARCHING
    # ------------------------------------------------------------------ #

    def test_search_by_title(self):
        """Test searching books by title keyword."""
        response = self.client.get(reverse('book-list'), {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_search_by_author_name(self):
        """Test searching books by author name keyword."""
        response = self.client.get(reverse('book-list'), {'search': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ------------------------------------------------------------------ #
    #  ORDERING
    # ------------------------------------------------------------------ #

    def test_ordering_by_title_asc(self):
        """Test ordering books by title ascending."""
        response = self.client.get(reverse('book-list'), {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_publication_year_desc(self):
        """Test ordering books by publication year descending."""
        response = self.client.get(
            reverse('book-list'), {'ordering': '-publication_year'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ------------------------------------------------------------------ #
    #  PERMISSIONS
    # ------------------------------------------------------------------ #

    def test_list_accessible_without_auth(self):
        """Test that the book list is accessible without authentication."""
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_accessible_without_auth(self):
        """Test that book detail is accessible without authentication."""
        response = self.client.get(
            reverse('book-detail', kwargs={'pk': self.book1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
