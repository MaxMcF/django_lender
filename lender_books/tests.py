from django.test import TestCase, RequestFactory
from .models import Book

class TestBookModel(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='A Sprinkle in Thyme', author='RL Burnside', year='1776', isbn='1234')
        Book.objects.create(title='My Cousin Lewis', author='John Ham', year='1969')
        Book.objects.create(title='The Lying, The Switch, and the War Robe', author='Beavis', year='2021')

    def test_book_titles(self):
        self.assertEqual(self.book.title, 'A Sprinkle in Thyme')

    def test_book_detail(self):
        book = Book.objects.get(title='A Sprinkle in Thyme')
        self.assertEqual(book.author, 'RL Burnside')

class TestBookViews(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.book_one = Book.objects.create(title='The First Book', author='Yes', year='2012')
        self.book_two = Book.objects.create(title='The Second Book', author='No', year='2016')

    def test_book_detail_view(self):
        from .views import books_detail_view
        request = self.request.get('')
        response = books_detail_view(request, f'{self.book_one.id}')
        self.assertIn(b'The First Book', response.content)

    def test_book_detail_status(self):
        from .views import books_detail_view
        request = self.request.get('')
        response = books_detail_view(request, f'{self.book_one.id}')
        self.assertEqual(200, response.status_code)
