from django.contrib import admin
from .models import Book, UserProfile, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'status', 'date_added')
    list_filter = ('status', 'author')
    search_fields = ('title', 'author', 'isbn')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'bio')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username')
