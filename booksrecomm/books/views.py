from django.views.generic import ListView
from .models import Book
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # show only books for the logged-in user
            return Book.objects.filter(user=self.request.user)
        else:
            # show all books to anonymous users
            return Book.objects.all()
