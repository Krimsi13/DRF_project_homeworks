from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer('lessons', many=True, read_only=True)
    # lesson = LessonSerializer(source='lessons', many=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, obj):
        return obj.lessons.all().count()

    # def get_count_lessons(self, instance):
    #     return instance.lessons.all().count()
