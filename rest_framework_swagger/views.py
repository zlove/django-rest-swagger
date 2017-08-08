from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

from . import renderers

def get_swagger_view(title=None, url=None, patterns=None, urlconf=None,
                     description='', public=False, renderer_classes=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    # assign to non-conflicting variable name, for closure
    if renderer_classes:
        _renderer_classes = renderer_classes
    else:
        _renderer_classes = (
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        )

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = _renderer_classes

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf,
                description=description,
            )
            schema = generator.get_schema(request=request, public=public)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()



def get_swagger_redoc_view(title=None, url=None, patterns=None, urlconf=None,
                           description='', public=False):
    """
    Returns schema view which renders Redoc browsable Swagger/OpenAPI.

    See: https://github.com/Rebilly/ReDoc
    """

    redoc_renderer_classes = (
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerRedocRenderer
    )

    return get_swagger_view(title, url, patterns, urlconf, description, public,
                            renderer_classes=redoc_renderer_classes)
