from django.urls import path
from .views import TrainCreateView, TrainSearchView

urlpatterns = [
    path('', TrainCreateView.as_view()),
    path('search/', TrainSearchView.as_view()),
]