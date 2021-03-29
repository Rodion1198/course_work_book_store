from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Author, Book, Cart, CartProduct, Customer, PublishingHouse
from .views import recalc_cart


User = get_user_model()


class StoreTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        image = SimpleUploadedFile('book_image.jpg', content=b'', content_type='image/jpg')
        self.publishing_house = PublishingHouse.objects.create(name='Test_publishing_house', info='Test_info')
        self.author = Author.objects.create(first_name='Victor', last_name='Doss', bio='cool author',
                                            date_of_birth='1863-06-07', date_of_death='1934-02-08')
        self.book = Book.objects.create(
            title="Test Book",
            publication_year='1976',
            publishing_house=self.publishing_house,
            image=image,
            author=self.author,
            price=Decimal('2000.00'),
            description='test description',
            slug='1237635278394',
            quantity='5',
        )
        self.customer = Customer.objects.create(user=self.user, phone='11111111', address='adres')
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            book=self.book,
        )

    def test_add_to_cart(self):
        self.cart.books.add(self.cart_product)   # add cart product to cart
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.books.all())   # checks that the object is in the cart
        self.assertEqual(self.cart.books.count(), 1)              # quantity in cart=1, duplicate check
        self.assertEqual(self.cart.final_price, Decimal('2000.00'))   # check for cart price
