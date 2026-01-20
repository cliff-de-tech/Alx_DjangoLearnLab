# Permissions and Groups Setup Guide

## Overview
This document describes the permissions and groups system implemented in the bookshelf application for managing book operations.

## Custom Permissions

The following custom permissions have been defined in the `Book` model (`bookshelf/models.py`):

- **can_view**: Permission to view books
- **can_create**: Permission to create new books
- **can_edit**: Permission to edit existing books
- **can_delete**: Permission to delete books

These permissions are defined in the `Book` model's Meta class:

```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

## Recommended Groups Setup

### 1. Viewers Group
**Permissions:**
- can_view

**Purpose:** Users who can only view the book list.

### 2. Editors Group
**Permissions:**
- can_view
- can_create
- can_edit

**Purpose:** Users who can view, create, and edit books but cannot delete them.

### 3. Admins Group
**Permissions:**
- can_view
- can_create
- can_edit
- can_delete

**Purpose:** Users with full access to all book operations.

## Setting Up Groups and Permissions

### Via Django Admin

1. **Access Django Admin:**
   - Navigate to `/admin/`
   - Log in with superuser credentials

2. **Create Groups:**
   - Go to Authentication and Authorization → Groups
   - Click "Add Group"
   - Enter group name (e.g., "Viewers", "Editors", "Admins")
   - Select appropriate permissions from the "Available permissions" list
   - Look for permissions starting with "bookshelf | book |"
   - Move selected permissions to "Chosen permissions"
   - Click "Save"

3. **Assign Users to Groups:**
   - Go to Authentication and Authorization → Users
   - Select a user
   - Scroll to "Groups" section
   - Move desired groups from "Available groups" to "Chosen groups"
   - Click "Save"

### Via Django Shell

You can also set up groups programmatically:

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

# Get the Book content type
content_type = ContentType.objects.get_for_model(Book)

# Get permissions
can_view = Permission.objects.get(codename='can_view', content_type=content_type)
can_create = Permission.objects.get(codename='can_create', content_type=content_type)
can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Create Viewers group
viewers = Group.objects.create(name='Viewers')
viewers.permissions.add(can_view)

# Create Editors group
editors = Group.objects.create(name='Editors')
editors.permissions.add(can_view, can_create, can_edit)

# Create Admins group
admins = Group.objects.create(name='Admins')
admins.permissions.add(can_view, can_create, can_edit, can_delete)

# Assign a user to a group
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='example_user')
user.groups.add(editors)
```

## Views with Permission Enforcement

All book-related views are protected with the `@permission_required` decorator:

### book_list (bookshelf/views.py)
- **Permission Required:** `bookshelf.can_view`
- **Purpose:** Display list of all books
- **URL:** `/bookshelf/books/`

### book_create (bookshelf/views.py)
- **Permission Required:** `bookshelf.can_create`
- **Purpose:** Create a new book
- **URL:** `/bookshelf/books/create/`

### book_edit (bookshelf/views.py)
- **Permission Required:** `bookshelf.can_edit`
- **Purpose:** Edit an existing book
- **URL:** `/bookshelf/books/<id>/edit/`

### book_delete (bookshelf/views.py)
- **Permission Required:** `bookshelf.can_delete`
- **Purpose:** Delete a book
- **URL:** `/bookshelf/books/<id>/delete/`

## Permission Checks in Templates

The templates use Django's `perms` context variable to conditionally display action buttons based on user permissions:

```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}

{% if perms.bookshelf.can_edit %}
    <a href="{% url 'book_edit' book.pk %}">Edit</a>
{% endif %}

{% if perms.bookshelf.can_delete %}
    <a href="{% url 'book_delete' book.pk %}">Delete</a>
{% endif %}
```

## Testing the Permissions System

### Manual Testing Steps:

1. **Create test users:**
   ```bash
   python manage.py createsuperuser  # Create admin user if not exists
   ```

2. **Create groups via Django admin:**
   - Create "Viewers", "Editors", and "Admins" groups
   - Assign appropriate permissions to each group

3. **Create test users and assign to groups:**
   - Create users: viewer_user, editor_user, admin_user
   - Assign each to their respective group

4. **Test access:**
   - Log in as `viewer_user`:
     - Should see book list
     - Should NOT see "Add New Book" button
     - Should NOT see "Edit" or "Delete" buttons
   
   - Log in as `editor_user`:
     - Should see book list
     - Should see "Add New Book" button
     - Should see "Edit" button
     - Should NOT see "Delete" button
   
   - Log in as `admin_user`:
     - Should see all buttons and have full access

5. **Test direct URL access:**
   - Try accessing protected URLs directly without proper permissions
   - Should receive a 403 Forbidden error (Permission Denied)

## Security Notes

- The `raise_exception=True` parameter in `@permission_required` ensures that users without proper permissions receive a 403 error instead of being redirected to login
- All form submissions include CSRF tokens for protection against cross-site request forgery
- User input is validated through Django forms before being saved to the database
- Templates conditionally display actions based on user permissions to improve UX

## Troubleshooting

**Problem:** User has permission but still gets "Permission Denied"
- **Solution:** Check that the permission is correctly assigned to the user or their group
- Verify the permission codename matches exactly (e.g., 'bookshelf.can_view')

**Problem:** Permissions not appearing in admin
- **Solution:** Run migrations to ensure permissions are created: `python manage.py migrate`

**Problem:** Changes to groups not taking effect
- **Solution:** User may need to log out and log back in for group changes to take effect
