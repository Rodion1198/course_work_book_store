from rest_framework import serializers

from .models import Book, BookInstance, Order, OrderProduct


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ('id', 'book', 'order_product', 'status',)


class BookSerializer(serializers.ModelSerializer):
    book = BookInstanceSerializer(source="bookinstance_set", many=True)

    class Meta:
        many = True
        model = Book
        fields = ['id', 'title', 'price', 'description',
                  'publishing_house', 'author', 'genre', 'slug', 'book']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'book', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(source="orderproduct_set", many=True)

    class Meta:
        model = Order
        fields = ['id', 'email', 'first_name',
                  'last_name', 'phone', 'price', 'status', 'order_products']
