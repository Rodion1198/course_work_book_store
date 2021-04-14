from rest_framework import serializers

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio', 'date_of_birth', 'date_of_death']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class PublishingHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublishingHouse
        fields = ['id', 'name']


class BookBasicSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    publishing_house = PublishingHouseSerializer(read_only=True)

    class Meta:
        many = True
        model = Book
        fields = ('id', 'title', 'price', 'publication_year', 'image', 'description',
                  'publishing_house', 'author', 'genre', 'slug', 'quantity')


class BookBasicInstanceSerializer(serializers.ModelSerializer):
    book = BookBasicSerializer(read_only=True)

    class Meta:
        model = BookInstance
        fields = ('id', 'book', 'status')


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        many = True
        model = Book
        fields = ['id', 'title', 'price', 'publication_year', 'image', 'description',
                  'publishing_house', 'author', 'genre', 'slug', 'quantity']


class BookInstanceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        many = True
        model = BookInstance
        fields = ['id', 'book', 'status']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'book', 'email', 'first_name', 'last_name', 'phone', 'price', 'status')
