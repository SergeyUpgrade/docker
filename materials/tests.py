from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lessons, Courses
from users.models import User

class TestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="tets@test.ru")
        self.course = Courses.objects.create(name="Test Course", owner=self.user)
        self.lesson = Lessons.objects.create(name="Test Lesson", courses=self.course, video_url="youtube.com", owner=self.user)
        self.client.force_authenticate(user=self.user)


class LessonsTestCase(TestCase, APITestCase):


    def test_lessons_retrieve(self):
        url = reverse("materials:materials_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.lesson.name)

    def test_lesson_create(self):
        url = reverse('materials:materials_create')
        data = {
            'name': 'Test Lesson 2',
            'courses': self.course.pk,
            'video_url': 'youtube.com',
            'owner': self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:materials_update', args=(self.lesson.pk,))
        data = {
            'name': 'Updated Test Lesson',
        }
        response = self.client.patch(url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lessons.objects.get(pk=self.lesson.pk).name, 'Updated Test Lesson')

    def test_lesson_delete(self):
        url = reverse('materials:materials_destroy', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.count(), 0)

class SubscriptionTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="tets@test.ru")
        self.course = Courses.objects.create(name="Test Course")
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):

        url = reverse('materials:subscription_create', args=(self.course.pk,))
        data = {
            'user': self.user.pk,
            'course_id': self.course.pk,
        }
        response = self.client.post(url, data=data)
        print("response.json:", response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка создана")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Подписка удалена")
