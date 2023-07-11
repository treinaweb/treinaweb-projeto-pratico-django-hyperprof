from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    data = {}
    if isinstance(exc, ValidationError):
        data["message"] = "Erro de validação"
        data["errors"] = response.data
    else:
        data["message"] = response.data.get("detail")
    return Response(data, status=response.status_code)
