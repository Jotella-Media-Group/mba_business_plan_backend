from core.utils.format_responses import format_response_data
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.response import Response


class CustomJsonRender(CamelCaseJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = None
        if renderer_context:
            response: Response = renderer_context["response"]
            status_code = response.status_code

        data = format_response_data(data, status_code)
        return super().render(data, accepted_media_type, renderer_context)
