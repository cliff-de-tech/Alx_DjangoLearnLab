from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends Django's UserAdmin to include custom fields.
    """
    model = CustomUser
    
    # Fields to display in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Fields to filter by in the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_of_birth')
    
    # Fields to search by
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Ordering of users in the list view
    ordering = ('username',)
    
    # Fieldsets for the user detail/edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'profile_photo')}),
    )


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')


# Register models with their admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)

