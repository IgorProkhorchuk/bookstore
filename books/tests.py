from django.test import TestCase
from django.urls import reverse
from .models import Book, Review
from django.contrib.auth import get_user_model

class BookTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username = 'User1',
            email = 'user1@mail.com',
            password = 'password123',
        )

        self.book = Book.objects.create(
            title = "Book title",
            author = "Book author",
            price = '25.00',
        )

        self.review = Review.objects.create(
            book = self.book,
            author = self.user,
            review = 'Such a book!!',
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Book title')
        self.assertEqual(f'{self.book.author}', 'Book author')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book title')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Book title')
        self.assertContains(response, 'Such a book!!')
        self.assertTemplateUsed(response, 'books/book_detail.html')


