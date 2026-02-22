from django.urls import path
from .views import BookSeatView, MyBookingsView

urlpatterns = [
    path('', BookSeatView.as_view()),
    path('my/', MyBookingsView.as_view()),
]