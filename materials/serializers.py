from rest_framework.serializers import ModelSerializer, URLField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_link


class LessonSerializer(ModelSerializer):
    link_to_video = URLField(validators=[validate_link])

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
