from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('book/', views.BookList.as_view()),
    path('order/', views.OrderCreate.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
