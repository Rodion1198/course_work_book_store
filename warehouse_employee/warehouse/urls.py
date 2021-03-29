from django.conf.urls import url
from django.urls import include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'book_instances', views.BookInstanceViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
