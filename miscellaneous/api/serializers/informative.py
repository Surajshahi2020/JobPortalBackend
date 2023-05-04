from rest_framework import serializers

from miscellaneous.models import InfoPage


class InfoPageSerializer(serializers.ModelSerializer):
    content = serializers.JSONField(default={})

    class Meta:
        model = InfoPage
        fields = [
            "id",
            "title",
            "slug",
            "content",
        ]
        extra_kwargs = {
            "slug": {
                "read_only": True,
            }
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        title = data.get("title")
        if InfoPage.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                {
                    "title": "Informative Post",
                    "message": "An info page with this title already exists.",
                }
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        content = dict(validated_data.pop("content"))
        return super().create(
            {
                **validated_data,
                "content": content,
            }
        )
