from rest_framework.renderers import JSONRenderer


class custom_render(JSONRenderer):
    # 重构render方法
    # TODO: 标准输出是怎样的格式
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            msg, code = 'success', 1 if isinstance(data, dict) else 500
            # 存在异常的情况下，重新构建返回内容
            if data.get('message') is not None:
                msg, code = data.get('message'), data.get('code')
                data = {}
            data = {"code": code, 'message': msg, 'data': data}
        return super().render(data, accepted_media_type, renderer_context)
