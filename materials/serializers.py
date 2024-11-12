from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Courses, Lessons


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'


class CoursesSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, courses):
        return courses.name.count()

    class Meta:
        model = Courses
        fields = ("name", "description", "lessons_count")


class CoursesDetailSerializer(ModelSerializer):
    count_lessons_of_courses = serializers.SerializerMethodField()
    lessons = LessonsSerializer(many=True, read_only=True)

    def get_count_lessons_of_courses(self, courses):
        return courses.lessons.count()

    class Meta:
        model = Courses
        fields = ('name', 'count_lessons_of_courses', 'lessons')
