from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_lifecycle import AFTER_UPDATE, LifecycleModelMixin, hook


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
    slug = models.SlugField(unique=True, blank=True, max_length=13, help_text=_("13 character unique number"))

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title


class Order(LifecycleModelMixin, models.Model):

    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, 'in_progress'),
        (STATUS_READY, 'is_ready'),
        (STATUS_COMPLETED, 'completed')
    )

    book = models.CharField(_('title'), max_length=100)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    phone = models.CharField(_("phone number"), max_length=100)
    price = models.DecimalField(_('price'), max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        # default=STATUS_IN_PROGRESS,
        help_text='order status'
    )

    def __str__(self):
        return f'Order: {self.first_name} {self.last_name}'

    @hook(AFTER_UPDATE, when='status', is_now="completed")
    def order_status_completed_email(self):
        send_mail(
            "Your order was completed!",
            "Your order was completed successfully!",
            "admin@admin.com",
            [f'{self.email}'],
            fail_silently=False
        )


class BookInstance(models.Model):

    class SellStatus(models.IntegerChoices):
        IN_STOCK = 1, _('In stock')
        SOLD = 2, _('Sold')

    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    status = models.PositiveSmallIntegerField(
        choices=SellStatus.choices, default=SellStatus.IN_STOCK, blank=True, help_text=_('Book status')
    )

    def __str__(self):
        return f"{self.id} ({self.book.title})"
