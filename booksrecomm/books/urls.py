from django.urls import path
from . import views
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, AllBookListView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView  
# from .views import ReviewCreateView, ReviewUpdateView  

urlpatterns = [

    path("books/", BookListView.as_view(), name="book_list"),
    path("all_books/", AllBookListView.as_view(), name="all_list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/add/", BookCreateView.as_view(), name="book-add"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-edit"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
        # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="books/login.html"), name="login"),
     path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    path("register/", views.register, name="register"),
# path('books/<int:book_id>/reviews/new/', ReviewCreateView.as_view(), name='reviewbook_create'),
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/<int:pk>/", views.review_detail, name="review_detail"),
    path("reviews/add/", views.review_create, name="review_create"),
    path("reviews/<int:pk>/edit/", views.review_edit, name="review_edit"),
    path('books/<int:pk>/add_review/', views.add_review, name='add_review'),
    path("reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),


]