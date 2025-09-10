# Register your models here.
from django.contrib import admin
from .models import Book
from .models import CustomUser

# Customize how Book is displayed in the admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns
    list_filter = ('publication_year', 'author')  # filter options on the right
    search_fields = ('title', 'author')  # adds a search box

class CustomUserAdmin(UserAdmin):
    # Display these fields in the admin list
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_superuser")

    # Add date_of_birth and profile_photo to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

    # for the create user page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
