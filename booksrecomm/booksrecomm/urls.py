from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Add this import
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  
    
]