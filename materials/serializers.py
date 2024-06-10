from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, obj):
        return obj.lessons.all().count()

    # def get_count_lessons(self, instance):
    #     return instance.lessons.all().count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
