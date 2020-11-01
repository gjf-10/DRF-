from django.urls import path

from day08_repeat import views

urlpatterns = [
    # 所有
    path('books/', views.BookAPIView.as_view()),
    # 单本
    path('books/<id>/', views.BookAPIView.as_view()),
]