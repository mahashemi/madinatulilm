from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import BookCategory, Book


def books_home(request):
    categories = BookCategory.objects.all()
    books = Book.objects.filter(is_active=True)
    context = {"categories": categories, "books": books}
    return render(request, "books/books_home.html", context)


def books_by_category(request, slug):
    category = get_object_or_404(BookCategory, slug=slug)
    books = category.books.filter(is_active=True)
    return render(request, "books/books_category.html", {"category": category, "books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True)
    return render(request, "books/book_detail.html", {"book": book})


def book_download(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True, is_downloadable=True)
    book.download_count += 1
    book.save(update_fields=["download_count"])
    return FileResponse(book.pdf_file.open(), as_attachment=True, filename=f"{book.title_en}.pdf")
