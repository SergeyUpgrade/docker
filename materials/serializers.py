from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Courses, Lessons


class CoursesSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class CoursesDetailSerializer(ModelSerializer):
    count_lessons_of_courses = SerializerMethodField()

    def get_count_lessons_of_courses(self, courses):
        return Courses.objects.filter(name=courses.name).count()
    class Meta:
        model = Courses
        fields = ('name', 'description', 'count_lessons_of_courses')
       # fields = ('name', 'count_lessons_of_courses')


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'
