from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from rest_framework.test import APIClient
from yorozu.models import Plan

from ..serializers.serializer_plan import PlanSerializer

PLAN_URL = reverse('yorozu:plan')
print(PLAN_URL)


class PublicPlanAPiTests(TestCase):
    '''プランAPIテスト'''

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_plan(self):
        res = self.client.get(PLAN_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivatePlanAPITests(TestCase):
    '''プライベートになっているかテスト'''

    def setUp(self):
        self.client() = APIClient()
        self.use = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass',
        )
        # self.cli
