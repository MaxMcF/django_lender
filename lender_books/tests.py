from django.test import TestCase, RequestFactory, Client
from .models import Book
from django.contrib.auth.models import User
from django.http.response import Http404

class TestBookModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='testing@example.org')
        self.user.set_password('1234')

        self.book = Book.objects.create(title='A Sprinkle in Thyme', 
            author='RL Burnside', 
            year='1776', 
            isbn='1234',
            user= self.user,
            )

        # Book.objects.create(title='My Cousin Lewis', author='John Ham', year='1969')
        # Book.objects.create(title='The Lying, The Switch, and the War Robe', author='Beavis', year='2021')

    def test_book_title(self):
        self.assertEqual(self.book.title, 'A Sprinkle in Thyme')

    def test_book_author(self):
        self.assertEqual(self.book.author, 'RL Burnside')
    
    def test_book_year(self):
        self.assertEqual(self.book.year, '1776')
    
    def test_book_isbn(self):
        self.assertEqual(self.book.isbn, '1234')

    def test_book_user(self):
        self.assertEqual(self.book.user, self.user)

    def test_book_status_sets_default(self):
        self.assertEqual(self.book.status, 'checked-out')
    
    def test_book_detail(self):
        book = Book.objects.get(title='A Sprinkle in Thyme')
        self.assertEqual(book.author, 'RL Burnside')

class TestBookViews(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = User.objects.create(username='test', email='testing@example.com')
        self.user.set_password('4321')
        self.book_one = Book.objects.create(title='The First Book', author='Yes', year='2012', user=self.user)
        self.book_two = Book.objects.create(title='The Second Book', author='No', year='2016', user=self.user)
        self.request.user = self.user

    def test_book_detail_view(self):
        from .views import books_detail_view
        request = self.request
        response = books_detail_view(request, f'{self.book_one.id}')
        self.assertIn(b'The First Book', response.content)

    def test_book_detail_status(self):
        from .views import books_detail_view
        request = self.request
        response = books_detail_view(request, f'{self.book_one.id}')
        self.assertEqual(200, response.status_code)
    
    def test_book_detail_view_fail_on_other_user(self):
        from .views import books_detail_view
        request = self.request
        request.user = User.objects.create(username='test2', email='another@test.com')
        request.user.set_password('4321')
        with self.assertRaises(Http404):
            response = books_detail_view(request, f'{self.book_one.id}')

    # def test_book_detail_date_filter(self):
    #     from .views import books_detail_view
    #     request = self.request.get('')
    #     request.user = self.user
    #     response = books_detail_view(request, f'{self.book_one.id}')
        
    #     self.assertIn(b'Created: Today.', response.content)


class TestLogin(TestCase):
    def setUp(self):
        self.c = Client()

    def test_login_newly_made_user(self):
        self.user = User.objects.create(username='tester', email='testinganother@web.com')
        self.user.set_password('5555')
        response = self.c.post('/login/', {'username': 'tester', 'password': '5555'})
        self.assertEqual(200, response.status_code)


