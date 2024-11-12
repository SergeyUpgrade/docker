from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from materials.models import Courses, Lessons
from materials.serializers import CoursesSerializer, LessonsSerializer, CoursesDetailSerializer


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoursesDetailSerializer
        return CoursesSerializer


class LessonsCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsRetrieveAPIView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsUpdateAPIView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
