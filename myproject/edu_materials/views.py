from rest_framework import generics, permissions, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """контроллер-вьюсет для CRUD
     с правами для работы модераторов, немодераторов или владельцев курсов\лекций """
    serializer_class = CourseSerializer

    def get_permissions(self):
       """метод для разграничения прав доступа, формирует список
        прав  для немодератора, модератора или владельца"""
       if self.action == "create":
            self.permission_classes = (~IsModerator,)
       elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
       else:
            self.permission_classes = (IsModerator | IsOwner,)
       return super().get_permissions()

    def perform_create(self, serializer):
        """Метод для присваивания курса владельцу """
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_queryset(self):
        """Метод, позволяет получить список курсов для владельца """
        if not IsModerator().has_permission(self.request, self):
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание контроллера для создания лекции немодератором. """
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)

    def perform_create(self, serializer):
        """Метод для присваивания лекции владельцу. """
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Создание контроллера для вывода списка лекций,
     которые могут просматривать владельцы или модераторы """
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)

    def get_queryset(self):
        """Метод, позволяет получить список лекции владельца """
        if not IsModerator().has_permission(self.request, self):
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс, позволяет модератору или владельцу получить детали лекции """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс, позволяет модератору или владельцу редактировать лекцию """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс, позволяет немодератору или владельцу удалить лекцию """
    queryset = Lesson.objects.all()
    permission_classes = (~IsModerator | IsOwner,)
