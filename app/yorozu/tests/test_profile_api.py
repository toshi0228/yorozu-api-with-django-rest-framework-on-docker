from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from yorozu.models.profile import Profile
from yorozu.serializers.serializer_profile import ProfileSerializer


PROFILE_URL = reverse("yorozu:profile-list")


def sample_profile(user, **params):
    '''サンプルのプロフィールを作成する'''

    defaults = {
        'account_id': "id",
        'yorozu_id': 'sampleId',
        'nickname': 'サンプルニックネーム',
        'yorozuya_name': 'よろずや',
        'profile_description': 'サンプルテキスト',
        'profile_image': '',
        'plan_thumbnail_image': '',
    }
    defaults.update(user=user, **defaults)

    return Profile.objects.create(user=user, **defaults)


# todo
class PublicProfileApiTests(TestCase):
    '''誰でもプロフィールを表示できるかテスト'''

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_profile(self):
        """プロフィールが表示されるかテスト"""
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


# todo
class PrivateProfileApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.com', 'testpass')
        self.client.force_authenticate(self.user)
