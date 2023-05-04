from miscellaneous.models import CommonImage
from common.pagination import CustomPagination
from rest_framework import generics
from miscellaneous.api.serializers.image import ImageSerializer
from rest_framework.response import Response
from common.permissions import (
    IsAuthenticated,
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema_view(
    post=extend_schema(
        description="Image Upload Api",
        summary="Refer To Schemas At Bottom",
        request=ImageSerializer,
        responses={
            200: {},
            422: {},
        },
        tags=["Image Upload Api"],
    ),
)
class ImageUploadView(generics.CreateAPIView):
    queryset = CommonImage.objects.all()
    serializer_class = ImageSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {
                "title": "Image Upload",
                "message": "Image uploaded successfully!",
                "data": super().create(request, *args, **kwargs).data,
            }
        )
