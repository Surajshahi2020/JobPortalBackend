from rest_framework import serializers
from miscellaneous.models import CommonImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonImage
        fields = [
            "image",
            "directory",
            "title",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if "image" not in data:
            raise serializers.ValidationError(
                {
                    "title": "Image Upload",
                    "message": "Image field is required!",
                }
            )

        return super().is_valid(raise_exception=raise_exception)
