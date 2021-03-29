from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.base import View

from .forms import LoginForm, OrderForm, RegistrationForm
from .mixins import CartMixin
from .models import Author, Book, CartProduct, Customer, Genre, Order, PublishingHouse
from .utils import recalc_cart


class BookListView(CartMixin, generic.ListView):

    def get(self, request, *args, **kwargs):

        books = Book.objects.all()
        author = Author.objects.all()
        publishing_house = PublishingHouse.objects.all()
        genre = Genre.objects.all()
        context = {
            'books': books,
            'author': author,
            'publishing_house': publishing_house,
            'genre': genre,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class BookDetailView(CartMixin, generic.DetailView):
    model = Book
    template_name = 'store/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.get_object().author.__class__.objects.all()
        context['publishing_house'] = self.get_object().publishing_house.__class__.objects.all()
        context['genre'] = Genre.objects.all()
        context['cart'] = self.cart
        return context


class AuthorListView(CartMixin, generic.ListView):
    model = Author
    paginate_by = 10
    template_name = 'store/author_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.all()
        context['publishing_house'] = PublishingHouse.objects.all()
        context['genre'] = Genre.objects.all()
        context['cart'] = self.cart
        return context


class AuthorDetailView(CartMixin, generic.DetailView):
    model = Author
    template_name = 'store/author_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class PublishingHouseListView(CartMixin, generic.ListView):
    model = PublishingHouse
    paginate_by = 10
    template_name = 'store/publish_house_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.all()
        context['publishing_house'] = PublishingHouse.objects.all()
        context['genre'] = Genre.objects.all()
        context['cart'] = self.cart
        return context


class PublishingHouseDetailView(CartMixin, generic.DetailView):
    model = PublishingHouse
    template_name = 'store/publish_house_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class GenreListView(CartMixin, generic.ListView):
    model = Genre
    paginate_by = 10
    template_name = 'store/genre_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.all()
        context['publishing_house'] = PublishingHouse.objects.all()
        context['genre'] = Genre.objects.all()
        context['cart'] = self.cart
        return context


class GenreDetailView(CartMixin, generic.DetailView):
    model = Genre
    template_name = 'store/genre_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, generic.View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        books = Book.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, book=books
        )
        if created:
            self.cart.books.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        book = Book.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, book=book
        )
        self.cart.books.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        book = Book.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, book=book
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'store/cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form
        }
        return render(request, 'store/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart,
        }
        return render(request, 'registration/login.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'registration/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(
                username=new_user.username, password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
            'cart': self.cart
        }
        return render(request, 'registration/registration.html', context)


class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        return render(request, 'store/profile.html', {'orders': orders, 'cart': self.cart})
