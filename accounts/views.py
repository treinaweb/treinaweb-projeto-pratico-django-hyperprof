from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView


class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_205_RESET_CONTENT)
