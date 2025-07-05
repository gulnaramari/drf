from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.permissions import IsModerator, IsOwner
from users.models import Subscription
from .paginators import LMSPagination
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, DocNoPermissionSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер-вьюсет для CRUD
    с правами для работы модераторов, немодераторов или владельцев курсов, лекций"""

    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    pagination_class = LMSPagination

    def get_permissions(self):
        """Метод для разграничения прав доступа, формирует список
        прав  для немодератора, модератора или владельца"""
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        else:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод для присваивания курса владельцу"""
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_queryset(self):
        """Метод, позволяет получить список курсов для владельца"""
        if not IsModerator().has_permission(self.request, self):
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()




@extend_schema(
    responses={
        status.HTTP_201_CREATED: LessonSerializer,
        status.HTTP_403_FORBIDDEN: DocNoPermissionSerializer,
    },
)
class LessonCreateAPIView(generics.CreateAPIView):
    """Создание контроллера для создания лекции немодератором."""

    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)
    queryset = Lesson.objects.all().order_by("id")

    def perform_create(self, serializer):
        """Метод для присваивания лекции владельцу."""
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Создание контроллера для вывода списка лекций,
    которые могут просматривать владельцы или модераторы"""

    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)
    pagination_class = LMSPagination

    def get_queryset(self):
        """Метод, позволяет получить список лекции владельца"""
        if not IsModerator().has_permission(self.request, self):
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс, позволяет модератору или владельцу получить детали лекции"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс, позволяет модератору или владельцу редактировать лекцию"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс, позволяет немодератору или владельцу удалить лекцию"""

    queryset = Lesson.objects.all().order_by("id")
    permission_classes = (~IsModerator | IsOwner,)
