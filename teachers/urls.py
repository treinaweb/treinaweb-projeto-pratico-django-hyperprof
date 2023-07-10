from django.urls import path

from .views import TeacherList

app_name = "teachers"
urlpatterns = [
    path("professores", TeacherList.as_view(), name="list"),
]
