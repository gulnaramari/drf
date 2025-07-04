from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import URLValidator


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example 1",
            value={
                "video_url": "http://youtube.com/your-lesson",
                "name": "string",
                "description": "string",
                "preview": "string",
                "course": 0,
            },
            request_only=True,
        ),
    ]
)
class LessonSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели лекции"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [URLValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    """Создание кастомного сериализатора для модели курса
    с дополнительными полями и вложенным сериализатором по лекции"""

    amount_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, course):
        """Calculating amount of lessons of a course."""
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """Returns info whether the user is subscribed to the course or not."""
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "amount_of_lessons",
            "lessons",
            "is_subscribed",
        )
class DocSubSerializer(serializers.Serializer):
    subscribe = serializers.BooleanField()

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Subscribe",
            value={
                "message": "Вы успешно подписаны на 'Course name'",
            },
            response_only=True,
        ),
        OpenApiExample(
            "Unsubscribe",
            value={
                "message": "Ваша подписка на 'Course name' аннулирована",
            },
            response_only=True,
        ),
    ]
)
class DocSubResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class DocNoPermissionSerializer(serializers.Serializer):
    detail = serializers.CharField(default="У вас нет права на это действие")
