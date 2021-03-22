from django.contrib import admin

from .models import Author, Book, Cart, CartProduct, Customer, Genre, Order, PublishingHouse


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Genre)
admin.site.register(Order)
