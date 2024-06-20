from rest_framework.serializers import ModelSerializer, URLField
from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
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
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, obj):
        return obj.lessons.all().count()

    # def get_count_lessons(self, instance):
    #     return instance.lessons.all().count()

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
