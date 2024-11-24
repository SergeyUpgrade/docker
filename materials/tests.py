from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lessons, Courses
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admiv@sky.pro")
        self.lesson = Lessons.objects.create(name="Русский", video_url="youtube.com")
        self.client.force_authenticate(user=self.user)

    def test_lessons_retrieve(self):
        url = reverse("materials:materials_list", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
