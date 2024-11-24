from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Courses, Lessons, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (CoursesDetailSerializer, CoursesSerializer,
                                   LessonsSerializer, SubscriptionSerializer)
from users.permissions import IsModer, IsOwner


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CoursesDetailSerializer
        return CoursesSerializer

    def perform_create(self, serializer):
        courses = serializer.save()
        courses.owner = self.request.user
        courses.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in {"update", "retrieve"}:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

class LessonsCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lessons = serializer.save()
        lessons.owner = self.request.user
        lessons.save()


class LessonsListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    pagination_class = CustomPagination


class LessonsRetrieveAPIView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonsUpdateAPIView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonsDestroyAPIView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsOwner)

class SubscriptionAPIView(APIView):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, course_id, *args, **kwargs):

        user = request.user

        course_item = get_object_or_404(Courses, id=course_id)

        subs_item = Subscription.objects.filter(course=course_item, user=user)


        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(course=course_item, user=user)
            message = 'Подписка создана'

        return Response({'message': message})


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer