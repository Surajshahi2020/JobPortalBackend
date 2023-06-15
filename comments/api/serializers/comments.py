from rest_framework import serializers
from comments.models import Comments
from common.utils import validate_uuid
from login.models import Job


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "id",
            "job",
            "body",
            "created_at",
            "creator",
        ]


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "id",
            "job",
            "body",
            "parent",
        ]

    def is_valid(self, *, raise_exception=False):
        print(7777777777777, Job.objects.all().values("id"))
        data = self.initial_data
        print(data)
        if not data.get("job", "").strip():
            raise serializers.ValidationError(
                {
                    "title": "Comments",
                    "message": "Job is required field",
                }
            )
        if not data.get("body", "").strip():
            raise serializers.ValidationError(
                {
                    "title": "Comments",
                    "message": "Body field is required and cannot be empty!",
                }
            )
        if data.get("parent") != "" and not validate_uuid(data["parent"]):
            raise serializers.ValidationError(
                {
                    "title": "Comments",
                    "message": "Invalid UUID in Parent field!",
                }
            )

        job = Job.objects.filter(id=data.get("job"))
        if not job.exists():
            raise serializers.ValidationError(
                {
                    "title": "Comments",
                    "message": "Job does not exist",
                }
            )

        return super().is_valid(raise_exception=raise_exception)


class EditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "body",
        ]
