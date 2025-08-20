from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Book, Review
from .forms import BookForm, ReviewForm, UserCreationForm, SignUpForm
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
class AllBookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 10  # Number of books per page

    def get_queryset(self):
        return Book.objects.all()  # Show all books regardless of user
class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews_list = book.reviews.all()  # get all reviews for this book
        paginator = Paginator(reviews_list, 5)  # 5 reviews per page

        page_number = self.request.GET.get('page')
        reviews_page = paginator.get_page(page_number)

        context['reviews_page'] = reviews_page
        return context

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        # Optional: allow all to view but restrict editing elsewhere
        return book
# class BookDetailView(DetailView):
#     model = Book
#     template_name = "books/book_detail.html"
#     context_object_name = "book"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reviews'] = Review.objects.filter(book=self.object)
#         return context

#     def get_object(self, queryset=None):
#         book = super().get_object(queryset)
#         # Optional: allow all to view but restrict editing elsewhere
#         return book

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the logged-in user
        return super().form_valid(form)
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
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
# Anyone can view reviews
def review_list(request):
    reviews = Review.objects.all()
    return render(request, "books/review_list.html", {"reviews": reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, "books/review_detail.html", {"review": review})

# Only logged-in users can create/edit/delete
@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("review_list")
    else:
        form = ReviewForm()
    return render(request, "books/review_form.html", {"form": form})

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("review_detail", pk=pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "books/review_form.html", {"form": form})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("review_list")
    return render(request, "books/review_confirm_delete.html", {"review": review})
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect("book_detail", pk=pk)
    else:
        form = ReviewForm()
    return render(request, "books/review_form.html", {"form": form, "book": book})