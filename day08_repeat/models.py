from django.db import models

# Create your models here.


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    publish = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    author = models.CharField(max_length=50)
    class Meta:
        db_table = "t_book"
        verbose_name = "书"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.book_name