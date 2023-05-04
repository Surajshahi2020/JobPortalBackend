from rest_framework import serializers

from miscellaneous.models import InfoPage


class InfoPageSerializer(serializers.ModelSerializer):
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
            },
            "title": {"validators": []},
        }

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        title = validated_data.get("title")
        inf = InfoPage.objects.filter(title=title)
        if inf.exists():
            inf.update(**validated_data)
            return inf.first()
        
        return super().create(validated_data)
