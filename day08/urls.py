from django.urls import path

from day08 import views

urlpatterns = [
    path('teachers/',views.TeacherAPIView.as_view()),
    path('teachers/<id>/',views.TeacherAPIView.as_view())
]