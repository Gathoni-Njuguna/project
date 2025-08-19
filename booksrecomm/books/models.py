from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('want_to_read', 'Want to Read'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, db_index=True, blank=True)
    total_pages = models.PositiveIntegerField(null=True, blank=True)
    current_page = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='want_to_read'
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.title} by {self.author}"
    
    # def get_absolute_url(self):
    #     return reverse('book_detail', kwargs={'pk': self.pk})
    
    # def progress_percentage(self):
    #     if self.total_pages > 0:
    #         return round((self.current_page / self.total_pages) * 100)
    #     return 0
    
    class Meta:
        ordering = ['-date_added']
        unique_together = ['user', 'isbn'] 
        verbose_name = 'Book'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'username': self.user.username})
    
class Review(models.Model):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    book= models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
    class Meta:
        unique_together = ['book', 'user']
        ordering = ['-created_at']