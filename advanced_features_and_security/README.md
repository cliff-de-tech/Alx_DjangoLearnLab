# Advanced Features and Security - Django Project

## Task 0: Custom User Model Implementation

This project demonstrates the implementation of a custom user model in Django by extending the `AbstractUser` class.

### Custom User Model Features

The custom user model (`CustomUser`) includes the following additional fields beyond Django's default user model:

1. **date_of_birth**: A date field to store the user's birth date (optional)
2. **profile_photo**: An image field to store user profile photos (optional)

### Implementation Details

#### 1. Custom User Model (`bookshelf/models.py`)
- **CustomUser**: Extends `AbstractUser` with additional fields
- **CustomUserManager**: Custom manager that handles user creation with the new fields
  - `create_user()`: Creates regular users
  - `create_superuser()`: Creates admin users with elevated permissions

#### 2. Settings Configuration (`LibraryProject/settings.py`)
- `AUTH_USER_MODEL = 'bookshelf.CustomUser'`: Configures Django to use the custom user model
- `MEDIA_URL` and `MEDIA_ROOT`: Configured to handle profile photo uploads

#### 3. Admin Configuration (`bookshelf/admin.py`)
- **CustomUserAdmin**: Extends Django's `UserAdmin` to manage custom fields
- Configured with:
  - Custom list display showing username, email, date_of_birth, and staff status
  - Filters for staff status, active status, and date of birth
  - Search functionality for username, email, and names
  - Fieldsets for adding and editing users with custom fields

#### 4. Updated References (`relationship_app/models.py`)
- Updated `UserProfile` model to reference `settings.AUTH_USER_MODEL` instead of `User`
- Updated signal receivers to use the custom user model

### Database Setup

All migrations have been created and applied successfully. The database is configured with:
- Custom user table with additional fields
- All standard Django authentication tables
- Related app models (Author, Book, Library, Librarian, UserProfile)

### Dependencies

- Django 6.0.1
- Pillow (for ImageField support)

### Next Steps

To create a superuser, run:
```bash
python manage.py createsuperuser
```

You will be able to add the date_of_birth and profile_photo through the Django admin interface after creating the user.
