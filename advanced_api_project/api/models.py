from django.db import models

# Create your models here.

class Author(models.Model):
    # Stores the author’s name
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Book title
    title = models.CharField(max_length=200)
    # Year of publication
    publication_year = models.IntegerField()
    # Foreign key linking Book to Author (one-to-many)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
