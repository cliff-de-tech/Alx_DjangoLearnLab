import datetime
from rest_framework import serializers
from .models import Author, Book


# BookSerializer handles serialization/deserialization of Book instances.
# It includes custom validation to ensure publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields: title, publication_year, and author.
    Includes custom validation on publication_year to prevent future dates.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validation: Ensure the publication year is not in the future.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "The publication year cannot be in the future."
            )
        return value


# AuthorSerializer handles serialization of Author instances.
# It nests a BookSerializer to dynamically serialize all related books,
# leveraging the 'books' reverse relationship defined by the ForeignKey
# on the Book model (related_name='books').
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    - name: The author's name.
    - books: A nested BookSerializer that serializes all books
      related to this author via the one-to-many relationship.
      'many=True' indicates multiple books can belong to one author.
      'read_only=True' means books are included in read responses
      but are not expected in write (create/update) requests for Author.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
