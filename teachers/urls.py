from django.urls import path

from .views import TeacherDetail, TeacherList

app_name = "teachers"
urlpatterns = [
    path("professores", TeacherList.as_view(), name="list"),
    path("professores/<int:pk>", TeacherDetail.as_view(), name="detail"),
]
