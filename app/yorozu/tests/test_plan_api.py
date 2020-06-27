from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from rest_framework.test import APIClient
from yorozu.models import Plan, Profile

from ..serializers.serializer_plan import PlanSerializer

PLAN_URL = reverse('yorozu:plan')

# プランのテストの時に必要


def sample_user(email='test2@gmail.com', password='testpass'):
    """サンプルユーザーを作成する"""
    return get_user_model().objects.create_user(email, password)


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
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass',
        )
        self.client.force_authenticate(self.user)

    def test_create_plan_successfull(self):
        '''プランを作成する'''

        # プランは、profileの主キーのyorozu_idと紐付いているので、先にprfoileを作成する
        profile = Profile.objects.create(account_id=sample_user().id,
                                         yorozu_id="SampleYorozuId", nickname="テステス", yorozuya_name="テスト屋")

        payload = {'yorozuyaProfileId': profile.yorozu_id,
                   'title': 'タイトル', 'description': 'テストの説明', 'image': '', 'price': 2, 'tag': ["tag"]}

        self.client.post(PLAN_URL, payload)
        exists = Plan.objects.filter(
            title='タイトル').exists()
        self.assertTrue(exists)

    def test_create_plan_invalid(self):
        '''プラン作成の失敗のテスト'''

        payload = {'yorozuyaProfileId': "",
                   'title': 'タイトル', 'description': 'テストの説明', 'image': '', 'price': 2, 'tag': ["tag"]}
        res = self.client.post(PLAN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
