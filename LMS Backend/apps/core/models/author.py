from django.db import models

class Author(models.Model):
    """
    Represents an author of a book.
    """
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name'] # Optional: Order authors alphabetically by default