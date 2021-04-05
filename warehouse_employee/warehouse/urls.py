from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'order', views.OrderViewSet)
router.register(r'author', views.AuthorViewSet)
router.register(r'publishing-house', views.PublishingHouseViewSet)
router.register(r'genre', views.GenreViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'book-instance', views.BookInstanceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('books/', views.BookBasicInstanceList.as_view()),

]
