from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'total_pages', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_pages'].widget.attrs['min'] = 1
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['class'] = 'form-select'