from django.http import HttpResponse

from rest_framework import viewsets

from .models import Book, BookInstance, Order, OrderProduct
from .serializers import BookInstanceSerializer, BookSerializer, OrderProductSerializer, OrderSerializer


def index(request):
    return HttpResponse("Hello, world the second project!!!!")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all().order_by('book__title')
    serializer_class = BookInstanceSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all().order_by('order')
    serializer_class = OrderProductSerializer
