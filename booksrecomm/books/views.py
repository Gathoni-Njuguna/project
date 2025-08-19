from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Book, Review
from .forms import BookForm, ReviewForm, UserCreationForm, SignUpForm
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 10  # Number of books per page

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # show only books for the logged-in user
            return Book.objects.filter(user=self.request.user)
        else:
            # show all books to anonymous users
            return Book.objects.all()
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        if book.user != self.request.user:
            raise Http404("You do not have permission to view this book.")
        return book
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the logged-in user
        return super().form_valid(form)
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
    success_url = reverse_lazy('book_list')

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        if book.user != self.request.user:
            raise Http404("You do not have permission to edit this book.")
        return book
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def test_func(self):
        book = self.get_object()
        return book.user == self.request.user

# Add to URL patterns
def home_redirect(request):
    return redirect('book_list')
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("book_list")
    else:
        form = SignUpForm()
    return render(request, "books/register.html", {"form": form})
def login_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Login successful!")
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "books/login.html", {"form": form})