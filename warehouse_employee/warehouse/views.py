from rest_framework import generics, viewsets
from rest_framework import mixins

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse
from .serializers import AuthorSerializer, BookBasicInstanceSerializer, BookInstanceSerializer, BookSerializer, \
    GenreSerializer, OrderSerializer, PublishingHouseSerializer


class BookBasicInstanceList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BookInstance.objects.order_by('book__title', 'book__author')
    serializer_class = BookBasicInstanceSerializer
    # paginator = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class PublishingHouseViewSet(viewsets.ModelViewSet):
    queryset = PublishingHouse.objects.all().order_by('id')
    serializer_class = PublishingHouseSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all().order_by('id')
    serializer_class = BookInstanceSerializer
