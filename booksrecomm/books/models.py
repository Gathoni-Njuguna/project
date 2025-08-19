from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Book(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('want_to_read', 'Want to Read'),
    )
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
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
        unique_together = ['user_id', 'isbn'] 
        verbose_name = 'Book'
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'username': self.user.username})
    
class Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

    class Meta:
        unique_together = ['book_id', 'user_id']
        ordering = ['-date_created']