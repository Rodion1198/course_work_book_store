from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='base'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),

    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),

    path('change-qty/<str:slug>/', views.ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),

    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

    path('publish_house/', views.PublishingHouseListView.as_view(), name='publish_house_list'),
    path('publish_house/<int:pk>/', views.PublishingHouseDetailView.as_view(), name='publish_house_detail'),

    path('genre/', views.GenreListView.as_view(), name='genre_list'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail_page'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

]
