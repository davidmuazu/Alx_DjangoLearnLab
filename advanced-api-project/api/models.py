from django.db import models

# Create your models here.


class Author(models.Model):
    """
    Author model stores basic information about book authors.
    Each author can have multiple related books.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model stores information about books.
    Each book is linked to a single Author (one-to-many relationship).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
