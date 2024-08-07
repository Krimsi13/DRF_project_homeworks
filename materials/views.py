from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner

from materials.tasks import send_mail_of_update_course


class CourseViewSet(ModelViewSet):
    """Viewset for Course"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer, IsAuthenticated)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer & IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

# Вариант №1
    # def perform_update(self, serializer):
    #     course = serializer.save()
    #     email_list = []
    #
    #     subscrubers = course.subscribe.all()
    #     for subscruber in subscrubers:
    #         email = subscruber.user.email
    #         email_list.append(email)
    #
    #     send_mail_of_update_course.delay(email_list)
    #     course.save()

# Вариант №2
#     def update(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         send_mail_of_update_course.delay(course_id=course.id)
#
#         return super().update(request)

# Вариант №3
    def perform_update(self, serializer):
        course = serializer.save()
        send_mail_of_update_course.delay(course_id=course.id)


class LessonCreateApiView(CreateAPIView):
    """Create a new lesson"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    """List of Lessons"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Get one Lesson"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    """Update Lesson"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    """Delete Lesson"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class SubscriptionCreateAPIView(APIView):
    """Manager for Subscription"""
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            subs_item = Subscription(user=user, course=course_item)  # Создание подписки
            subs_item.save()
            message = 'Подписка добавлена'
        return Response({"message": message})
