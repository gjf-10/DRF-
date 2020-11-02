from django.urls import path

from app import views

urlpatterns = [
    path('v3/book/', views.BookAPIView2.as_view()),
    path('v3/book/<id>/', views.BookAPIView2.as_view()),
    path('book/', views.BookGenericAPIView.as_view()),
    path('book/<str:id>/', views.BookGenericAPIView.as_view())
]