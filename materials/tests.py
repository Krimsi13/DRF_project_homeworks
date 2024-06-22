from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Subscription, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru")
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            "title": "variables",
            "description": "types variables",
            "link_to_video": "https://www.youtube.com/"
        }
        response = self.client.post(
            "/materials/lessons/create/",
            data=data
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1,
             'link_to_video': 'https://www.youtube.com/',
             'title': 'variables',
             'description': 'types variables',
             'preview': None,
             'course': None,
             'owner': 1}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""

        Lesson.objects.create(
            title="list test",
            description="list test",
            link_to_video="https://www.youtube.com/"
        )

        response = self.client.get(
            "/materials/lessons/"
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results':
                 [
                     {'id': 3,
                      'link_to_video': 'https://www.youtube.com/',
                      'title': 'list test',
                      'description': 'list test',
                      'preview': None,
                      'course': None,
                      'owner': None}
                 ]
             }
        )

    def test_retrieve_lesson(self):
        """Тестирование вывода урока"""

        lesson = Lesson.objects.create(
            title="retrieve test",
            description="retrieve test",
            link_to_video="https://www.youtube.com/",
            owner=self.user
        )

        response = self.client.get(
            f"/materials/lessons/{lesson.id}/"
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 4,
             'link_to_video': 'https://www.youtube.com/',
             'title': 'retrieve test',
             'description': 'retrieve test',
             'preview': None,
             'course': None,
             'owner': 4}
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""

        lesson = Lesson.objects.create(
            title="before update test",
            description="before update test",
            link_to_video="https://www.youtube.com/",
            owner=self.user
        )

        data = {
            "title": "after update test",
            "description": "after update test"
        }

        response = self.client.patch(
            f"/materials/lessons/{lesson.id}/update/",
            data
        )

        # print(response.json())

        out_data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            out_data.get("title"),
            "after update test")

        self.assertEqual(
            out_data.get("description"),
            "after update test"
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        lesson = Lesson.objects.create(
            title="delete test",
            description="delete test",
            link_to_video="https://www.youtube.com/",
            owner=self.user
        )

        response = self.client.delete(
            f"/materials/lessons/{lesson.id}/delete/"
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Lesson.objects.all().exists()
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="test", description="test", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscriptions")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "Подписка добавлена"})

    def test_unsubscribe(self):
        url = reverse("materials:subscriptions")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Подписка удалена'})
