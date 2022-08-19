from rest_framework import status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exc, context):
    global message
    response = exception_handler(exc, context)  # 调用原本的异常处理函数
    if response:
        # 这个循环是取第一个错误的提示用于渲染
        for index, value in enumerate(response.data):
            if index == 0:
                key = value
                value = response.data[key]
                if isinstance(value, str):
                    message = value
                else:
                    message = key + " : " + value[0]
        if response is None:
            return Response({'code': 500, 'message': '服务器错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
        else:
            return Response({'code': 0, 'message': message}, status=response.status_code, exception=True)
