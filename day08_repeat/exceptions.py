from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

# 异常的起始调用是在 APIView的as_view()——>View的as_view()中的view中调用了APIView的dispatch方法
# 在dispatch中调用了异常处理
# try:
#     self.initial(request, *args, **kwargs)
#
#     # Get the appropriate handler method
#     if request.method.lower() in self.http_method_names:
#         handler = getattr(self, request.method.lower(),
#                           self.http_method_not_allowed)
#     else:
#         handler = self.http_method_not_allowed
#
#     response = handler(request, *args, **kwargs)
#
# except Exception as exc:
#     response = self.handle_exception(exc)


def exception_handler(exc, context):
    # error = "%s %s %s" % (context["view"], context["request"].method, exc)
    response = drf_exception_handler(exc, context)
    # 这里处理的异常报的错可能不好找。必要时可以把它删了让程序出错，看原因是什么
    if response is None:
        return Response({"error_message": "上帝请稍等，程序猿正在加紧处理中..."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 如果response不为空，说明异常已经被处理了
    return response