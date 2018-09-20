from django.shortcuts import render, get_object_or_404
from .models import Book


def books_list_view(request):
    if not request.user.is_authenticated:
        return render(request, 'base/base.html', status=403)

    books = Book.objects.filter(user__username=request.user.username)

    context = {
        'books': books
    }
    return render(request, 'books/books_list.html', context=context)

def books_detail_view(request, pk=None):

    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    book = get_object_or_404(Book, id=pk, user__id=request.user.id)

    context = {
        'book': book
    }
    return render(request, 'books/books_detail.html', context=context)