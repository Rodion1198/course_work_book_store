from django.db import models
from django.utils.translation import gettext_lazy as _


class PublishingHouse(models.Model):
    name = models.CharField(_("name"), max_length=100)

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
        return self.name


class Book(models.Model):
    title = models.CharField(_("title"), max_length=100)
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    description = models.TextField(_("description"), blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name=_("genre"))
    slug = models.SlugField(_(unique=True, blank=True))

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title


class Order(models.Model):

    class OrderStatus(models.IntegerChoices):
        STATUS_IN_PROGRESS = 1, _('in progress')
        STATUS_READY = 2, _('is ready')
        STATUS_COMPLETED = 3, _('completed')

    shop_order_id = models.IntegerField(_('shop order id'), help_text='Shop order id')
    order_date = models.CharField(_('order date'), max_length=20)
    shipped_date = models.DateField(_('shipped date'), help_text='Date when order moved to completed status')
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.STATUS_IN_PROGRESS, blank=True, help_text=_('Order status')
    )

    def __str__(self):
        return f'{self.shop_order_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(_('quantity'), help_text='Books quantity')

    def __str__(self):
        return f"{self.id} ({self.order.shop_order_id})"
