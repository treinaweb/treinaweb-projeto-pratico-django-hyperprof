from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"
urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
]
