from rest_framework import generics
from rest_framework import mixins

from .models import BookInstance, Order
from .serializers import BookInstanceSerializer, OrderSerializer


class BookList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
