from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    # if response is None:
    #     return Response({
    #         "error_message": "上帝请稍等， 程序猿正在加紧处理中..."
    #         },
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response