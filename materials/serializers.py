from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Courses, Lessons, Subscription
from materials.validators import validate_permitted_words


class LessonsSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_permitted_words])

    class Meta:
        model = Lessons
        fields = "__all__"


class CoursesSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lessons_count(self, courses):
        return courses.lessons.count()

    class Meta:
        model = Courses
        fields = "__all__"


class CoursesDetailSerializer(serializers.ModelSerializer):
    count_lessons_of_courses = serializers.SerializerMethodField()
    lessons = LessonsSerializer(many=True, read_only=True)
    subscription_sign = serializers.SerializerMethodField()

    def get_count_lessons_of_courses(self, courses):
        return courses.lessons.count()

    def get_subscription_sign(self, instance):
        user = self.context.get("request").user
        subscription = Subscription.objects.filter(user=user, course=instance).exists()
        return subscription

    class Meta:
        model = Courses
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
