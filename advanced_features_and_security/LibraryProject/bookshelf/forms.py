from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    Includes validation for all Book fields.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
        }
    
    def clean_publication_year(self):
        """Validate that publication year is reasonable."""
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2100):
            raise forms.ValidationError('Please enter a valid publication year between 1000 and 2100.')
        return year
