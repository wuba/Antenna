from collections import defaultdict

from rest_framework import status
from rest_framework.views import Response, exception_handler

# 定义默认错误代码和消息
DEFAULT_ERROR_CODE = 0
DEFAULT_SERVER_ERROR_MESSAGE = '服务器错误'
VALUE_ERROR_MESSAGE = '输入值有误'


def custom_exception_handler(exc, context):
    try:
        # 调用原本的异常处理函数
        response = exception_handler(exc, context)
    except Exception as e:
        print(repr(e))
        # 处理ValueError异常，并返回自定义消息
        return Response(
            {'code': DEFAULT_ERROR_CODE, 'message': VALUE_ERROR_MESSAGE},
            status=status.HTTP_400_BAD_REQUEST,
            exception=True
        )

    # 如果response为None，返回500服务器错误
    if response is None:
        return Response(
            {'code': DEFAULT_ERROR_CODE, 'message': DEFAULT_SERVER_ERROR_MESSAGE},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            exception=True
        )

    # 使用defaultdict简化消息生成过程
    message = defaultdict(str)
    for k, v in response.data.items():
        message[k] = f'{v if isinstance(v, str) else v[0]} '

    # 返回优化后的响应
    return Response(
        {'code': DEFAULT_ERROR_CODE, 'message': " ".join(message.values())},
        status=response.status_code,
        exception=True
    )
