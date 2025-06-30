from rest_framework import serializers

from .models import Course, Lesson, Subscription


class LessonSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели лекции"""
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Создание кастомного сериализатора для модели курса
    с дополнительными полями и вложенным сериализатором по лекции"""
    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_count_of_lessons(self, obj):
        """Метод расчета количества лекций этого курса."""
        return obj.lesson_set.count()

    def get_info_lessons(self, course):
        lessons = course.lesson_set.all()
        return LessonSerializer(lessons, read_only=True, many=True).data

    def get_is_subscribed(self, course):
        """Метод, который возвращает нам, подписан пользователь на этот курс или нет"""
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "preview",
            "count_of_lessons",
            "info_lessons",
            "is_subscribed"
        )


