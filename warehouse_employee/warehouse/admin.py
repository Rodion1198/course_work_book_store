from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Order, OrderProduct, PublishingHouse


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth', 'date_of_death']
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'publishing_house',
              'author', 'price', 'description', 'genre', 'slug']
    search_fields = ('title',)
    list_display = ('title', 'author')
    list_filter = ('author', 'publishing_house', 'genre')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fields = ['book', 'status', 'order_item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['email', 'first_name', 'last_name',
              'phone', 'price', 'status']
    actions = ['status']
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')


@admin.register(OrderProduct)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
