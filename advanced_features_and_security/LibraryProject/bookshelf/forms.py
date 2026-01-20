from django import forms
from .models import Book


class ExampleForm(forms.Form):
    """
    Example form for demonstrating form handling and validation.
    """
    name = forms.CharField(max_length=100, required=True, help_text='Enter your name')
    email = forms.EmailField(required=True, help_text='Enter your email address')
    message = forms.CharField(widget=forms.Textarea, required=True, help_text='Enter your message')
    
    def clean_name(self):
        """Validate that name doesn't contain special characters."""
        name = self.cleaned_data.get('name')
        if name and not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name should only contain letters and spaces.')
        return name


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
