from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_lifecycle import AFTER_CREATE, AFTER_UPDATE, LifecycleModelMixin, hook

User = get_user_model()


class PublishingHouse(models.Model):
    name = models.CharField(_("name"), max_length=100)
    info = models.TextField(_("info"), blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    bio = models.TextField(_("bio"), blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    date_of_death = models.DateField(_("date of death"), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Genre(models.Model):
    name = models.CharField(_("name"), max_length=200)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(_("title"), max_length=100)
    publication_year = models.IntegerField(_('year'))
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')   # noqa: DJ01
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    description = models.TextField(_("description"), blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name=_("genre"))
    slug = models.SlugField(unique=True, blank=True, max_length=13, help_text=_("13 character ISBN number"))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class Customer(LifecycleModelMixin, models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)   # noqa: DJ01
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)   # noqa: DJ01
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

    @hook(AFTER_CREATE)
    def order_status_create_email(self):
        send_mail(
            "Your registration",
            "Your register was successfully!",
            "admin@admin.com",
            [f'{self.user.email}'],
            fail_silently=False
        )


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    book = models.ForeignKey(Book, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Книги: {} (для корзины)".format(self.book.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.book.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    books = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Order(LifecycleModelMixin, models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)   # noqa: DJ01
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)   # noqa: DJ01
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)

    @hook(AFTER_UPDATE, when='status', is_now="new")
    def order_status_create_email(self):
        send_mail(
            "Your order was create",
            "Your order was create successfully!",
            "admin@admin.com",
            [f'{self.email}'],
            fail_silently=False
        )
