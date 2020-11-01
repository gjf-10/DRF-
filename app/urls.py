import rest_framework
from django.urls import path

from app import views

urlpatterns = [
    path('users/', views.index),
    path('users1/', views.UserView.as_view()),
    path('users2/<id>/', views.UserViewAPI.as_view()),
    path('users2/', views.UserViewAPI.as_view())
]