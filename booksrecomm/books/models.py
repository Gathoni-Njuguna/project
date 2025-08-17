from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Book(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('want_to_read', 'Want to Read'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, db_index=True)
    total_pages = models.PositiveIntegerField()
    current_page = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='want_to_read'
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})
    
    def progress_percentage(self):
        if self.total_pages > 0:
            return round((self.current_page / self.total_pages) * 100)
        return 0
    
    class Meta:
        ordering = ['-date_added']
        unique_together = ['user', 'isbn'] 
        verbose_name = 'Book'