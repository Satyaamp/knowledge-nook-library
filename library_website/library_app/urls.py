from django.urls import path
from .views import home, about, contact, book_seat

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('book/', book_seat, name='book_seat'),
]
