from rest_framework import status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exc, context):
    # TODO: 异常处理
    response = exception_handler(exc, context)  # 调用原本的异常处理函数
    if response is None:
        return Response({'code': 500, 'message': '服务器错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    message = ""
    for k, v in response.data.items():
        message += f'{k}: {v if isinstance(v, str) else v[0]} '
    return Response({'code': 0, 'message': message}, status=response.status_code, exception=True)
