from django.urls import path

from .views import StudentList

app_name = "students"
urlpatterns = [
    path("professores/<int:teacher_pk>/alunos", StudentList.as_view(), name="list"),
]
